import cv2
import pandas as pd
import numpy as np
import streamlit as st
from ultralytics import YOLO
from src.tracker import Tracker
# from Utils import tts
import sqlite3
from datetime import datetime

# Connect to SQLite database (creates the database if it doesn't exist)
conn = sqlite3.connect('Data/database.db', check_same_thread=False)
db_cursor = conn.cursor()  # Use 'db_cursor' to avoid conflicts

# Create table if it doesn't exist
db_cursor.execute('''
CREATE TABLE IF NOT EXISTS person_log (
    person_id INTEGER,
    status TEXT,
    timestamp TEXT
)
''')
conn.commit()

# Function to insert data into the SQLite3 database
def log_person_entry_exit(person_id, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_cursor.execute("INSERT INTO person_log (person_id, status, timestamp) VALUES (?, ?, ?)", (person_id, status, timestamp))
    conn.commit()

    
def peoplecounter():
# Load the YOLO model
    model = YOLO('yolov8s.pt')

    # live camera (Top-left, Top-right, Bottom-right, Bottom-left corners)
    area1 = [(365, 256), (603, 256), (603, 268), (365, 268)]
    area2 = [(365, 288), (603, 288), (603, 272), (365, 272)]
    # Define the areas for entry and exit detection
    # area1 = [(337, 388), (314, 390), (499, 469), (522, 462)]
    # area2 = [(304, 392), (275, 397), (448, 477), (479, 469)]

    # video5/video2/v11
    # area1 = [(600, 288), (574, 290), (770, 369), (782, 362)]
    # area2 = [(564, 292), (535, 297), (708, 377), (760, 369)]

    #v11    Top-right:   Top-left: Bottom-left: Bottom-right
    # area1 = [(550, 300), (520, 300), (710, 380), (730, 372)]
    # area2 = [(514, 302), (485, 307), (658, 387), (710, 376)]

    # area1 = [(515, 300), (653, 300), (653, 310), (515, 310)]
    # area2 = [(515, 330), (653, 330), (653, 320), (515, 320)]

    # Load COCO class names
    with open("coco.txt", "r") as my_file:
        data = my_file.read()
    class_list = data.split("\n")

    # Initialize tracker and variables for counting
    tracker = Tracker()
    people_entering = {}
    entering = set()
    people_exiting = {}
    exiting = set()

    # Streamlit UI components
    st.title("Person Detection and Counting")
    use_camera = st.checkbox("Use Live Camera")

    # Initialize video capture based on user input
    cap = None
    if use_camera:
        cap = cv2.VideoCapture(1)
        st.success('Successfully live camera open 👏👏!')
        # tts('Successfully live camera open ')
    else:
        uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "avi", "mov"])
        if uploaded_video is not None:
            cap = cv2.VideoCapture(uploaded_video.name)
            st.success('Successfully uploaded video 👏👏!')
            # tts('Successfully uploaded video!')

    if cap is not None:
        stframe = st.empty()

        count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            count += 1
            if count % 2 != 0:
                continue

            #frame = cv2.resize(frame, (1080, 500))
            #live camera
            frame = cv2.resize(frame, (900, 330))
                        #video5/video2
            # frame=cv2.resize(frame,(1140,450))
                 #v11
            # frame = cv2.resize(frame, (1050, 350))
                    #v2
            # frame=cv2.resize(frame,(1000,350))

            # Predict objects using YOLO
            results = model.predict(frame)

            # Extract person detections
            a = results[0].boxes.data
            px = pd.DataFrame(a).astype("float")

            list_of_boxes = []
            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = class_list[d]
                if 'person' in c:
                    list_of_boxes.append([x1, y1, x2, y2])

            #
            # Update tracker with person bounding boxes
            bbox_id = tracker.update(list_of_boxes)

            # Process each detected person
            for bbox in bbox_id:
                x3, y3, x4, y4, person_id = bbox

                # Detect people entering
                results = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
                if results >= 0:
                    people_entering[person_id] = (x4, y4)
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)

                if person_id in people_entering:
                    results1 = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
                    if results1 >= 0:
                        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                        cv2.circle(frame, (x4, y4), 4, (0, 255, 0), -1)
                        cv2.putText(frame, str(person_id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                        if person_id not in entering:
                            entering.add(person_id)
                            log_person_entry_exit(person_id, "entering")

                # Detect people exiting
                results2 = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
                if results2 >= 0:
                    people_exiting[person_id] = (x4, y4)
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)

                if person_id in people_exiting:
                    results3 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
                    if results3 >= 0:
                        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                        cv2.circle(frame, (x4, y4), 4, (255, 0, 255), -1)
                        cv2.putText(frame, str(person_id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                        if person_id not in exiting:
                            exiting.add(person_id)
                            log_person_entry_exit(person_id, "exiting")

            # Draw entry/exit areas
            cv2.polylines(frame, [np.array(area1, np.int32)], True, (255, 255, 255))
            cv2.putText(frame, 'area1', (504, 471), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
            cv2.polylines(frame, [np.array(area2, np.int32)], True, (255, 255, 255))
            cv2.putText(frame, 'area2', (466, 485), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)

            # Display the counts
            Enter = len(entering)
            Exit = len(exiting)

            cv2.putText(frame, 'Total Enter Person', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame, str(Enter), (210, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame, 'Total Exit Person', (30, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 1)
            cv2.putText(frame, str(Exit), (200, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 1)

            # Display the current date and time on the video frame
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, f'{current_time}', (680, 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)

            # Display the video in Streamlit
            stframe.image(frame, channels="BGR", use_column_width=True)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    peoplecounter()
