import cv2
import pandas as pd
import numpy as np
import streamlit as st
from ultralytics import YOLO
from src.tracker import Tracker
from Utils import tts
from datetime import datetime
import sqlite3
import torch
import platform


if platform.system() == "Windows":
    try:
        # COM-related import
        import win32com.client
        
        # COM-related functionality (e.g., Excel automation, Windows-specific tasks)
        st.write("Running on Windows with COM functionality.")
    except ImportError:
        st.error("COM technology is not available on this platform.")
else:
    st.error("COM technology is only supported on Windows. Running on: " + platform.system())
def initialize_db():
    try:
        conn = sqlite3.connect('Data/database.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS tracking_data (
                ID INTEGER PRIMARY KEY,
                EnteringTime TEXT,
                ExitingTime TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

# Insert new entry when a person is detected entering
def insert_entry(id, entering_time):
    try:
        conn = sqlite3.connect('Data/database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO tracking_data (ID, EnteringTime, ExitingTime)
            VALUES (?, ?, ?)
        ''', (id, entering_time, None))
        conn.commit()
        print(f"Inserted entry: ID={id}, EnteringTime={entering_time}")
    except sqlite3.Error as e:
        print(f"Error inserting entry: {e}")
    finally:
        conn.close()

# Update exit time for a person when detected exiting
def update_exit(id, exiting_time):
    try:
        conn = sqlite3.connect('Data/database.db')
        c = conn.cursor()
        c.execute('''
            UPDATE tracking_data
            SET ExitingTime = ?
            WHERE ID = ? AND ExitingTime IS NULL
        ''', (exiting_time, id))
        conn.commit()
        print(f"Updated exit: ID={id}, ExitingTime={exiting_time}")
    except sqlite3.Error as e:
        print(f"Error updating exit: {e}")
    finally:
        conn.close()

# Fetch the tracking data from the database
def fetch_data():
    try:
        conn = sqlite3.connect('Data/database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM tracking_data')
        data = c.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        conn.close()

# Delete all rows from the tracking data table
def delete_all_rows():
    try:
        conn = sqlite3.connect('Data/database.db')
        c = conn.cursor()
        c.execute('DELETE FROM tracking_data')
        conn.commit()
        print("Deleted all rows from tracking_data")
    except sqlite3.Error as e:
        print(f"Error deleting rows: {e}")
    finally:
        conn.close()

# Function to handle the person counter and video processing
def peoplecounter():
    # Load YOLO model
    device = torch.device('cpu')
    # model = torch.load('yolov10n.pt', map_location=device)
    model = YOLO('yolov10n.pt')
    area1 = [(337, 388), (314, 390), (499, 469), (522, 462)]
    area2 = [(304, 392), (275, 397), (448, 477), (479, 469)]

    initialize_db()

    # Load COCO class names
    with open("coco.txt", "r") as my_file:
        data = my_file.read()
    class_list = data.split("\n")

    # Initialize tracker and sets for tracking people entering and exiting
    tracker = Tracker()
    people_entering = {}
    entering = set()
    people_exiting = {}
    exiting = set()

    # Streamlit UI components
    st.title("Person Detection and Counting")
    option = st.radio("Select Video Source", ("Upload Video", "Live Camera"))

    # Handle video source selection
    cap = None
    if option == "Upload Video":
        uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "avi", "mov"])
        if uploaded_video is not None:
            cap = cv2.VideoCapture(uploaded_video.name)
            st.success('Successfully uploaded video 👏👏!')
            tts('Successfully uploaded video!')
    elif option == "Live Camera":
        cap = cv2.VideoCapture(0)
        st.success('Live camera activated!')
        tts('Live camera activated!')

    # Display the tracking data table
    st.subheader("Tracking Data")
    if st.button("Refresh Table"):
        data = fetch_data()
        if data:
            df = pd.DataFrame(data, columns=["ID", "EnteringTime", "ExitingTime"])
            st.dataframe(df)
        else:
            st.write("No data available")

    if st.button("Delete All Rows"):
        delete_all_rows()
        st.success("All rows deleted")
        st.rerun()

    # If a video stream is available, process frames
    if cap is not None and cap.isOpened():
        stframe = st.empty()
        count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            count += 1
            if count % 2 != 0:
                continue  # Skip every other frame for performance

            frame = cv2.resize(frame, (1080, 500))
            results = model.predict(frame)

            # Extract bounding boxes from the model's predictions
            px = pd.DataFrame(results[0].boxes.data).astype("float")

            list_of_boxes = []
            for index, row in px.iterrows():
                x1, y1, x2, y2 = map(int, row[:4])
                class_id = int(row[5])
                if 'person' in class_list[class_id]:
                    list_of_boxes.append([x1, y1, x2, y2])

            bbox_id = tracker.update(list_of_boxes)

            # Loop through bounding boxes and handle entering/exiting logic
            for bbox in bbox_id:
                x3, y3, x4, y4, id = bbox

                # Detect entering
                if cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False) >= 0:
                    if id not in people_entering:
                        people_entering[id] = (x4, y4)
                        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                        print(f"Person {id} entering detected")
                        insert_entry(id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                if id in people_entering and cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False) >= 0:
                    if id not in entering:
                        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                        entering.add(id)

                # Detect exiting
                if cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False) >= 0:
                    if id not in people_exiting:
                        people_exiting[id] = (x4, y4)
                        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                        print(f"Person {id} exiting detected")
                        update_exit(id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                if id in people_exiting and cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False) >= 0:
                    if id not in exiting:
                        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                        exiting.add(id)

            # Draw detection areas and person counts
            cv2.polylines(frame, [np.array(area1, np.int32)], True, (255, 255, 255))
            cv2.putText(frame, 'area1', (504, 471), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv2.polylines(frame, [np.array(area2, np.int32)], True, (255, 255, 255))
            cv2.putText(frame, 'area2', (466, 485), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

            Enter = len(entering)
            Exit = len(exiting)

            cv2.putText(frame, 'Total Enter Person', (30, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, str(Enter), (270, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, 'Total Exit Person', (30, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, str(Exit), (250, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

            # Add current date and time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, current_time, (10, 320), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 255), 1)

            # Display the video in Streamlit
            stframe.image(frame, channels="BGR", use_column_width=True)

        cap.release()
