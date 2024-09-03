# from src.tracker import Tracker
# from ultralytics import YOLO
# import streamlit as st
# import pandas as pd
# import numpy as np
# import time
# import cv2
# import sqlite3

# def initialize_db():
#     conn = sqlite3.connect('data/database.db')
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS tracking_data (
#             ID INTEGER PRIMARY KEY,
#             EnteringTime TEXT,
#             ExitingTime TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# def insert_entry(id, entering_time):
#     conn = sqlite3.connect('data/database.db')
#     c = conn.cursor()
#     c.execute('''
#         INSERT OR IGNORE INTO tracking_data (ID, EnteringTime, ExitingTime)
#         VALUES (?, ?, ?)
#     ''', (id, entering_time, None))
#     conn.commit()
#     conn.close()

# def update_exit(id, exiting_time):
#     conn = sqlite3.connect('data/database.db')
#     c = conn.cursor()
#     c.execute('''
#         UPDATE tracking_data
#         SET ExitingTime = ?
#         WHERE ID = ? AND ExitingTime IS NULL
#     ''', (exiting_time, id))
#     conn.commit()
#     conn.close()

# def get_count(condition):
#     conn = sqlite3.connect('data/database.db')
#     c = conn.cursor()
#     c.execute(f'SELECT COUNT(*) FROM tracking_data WHERE {condition}')
#     count = c.fetchone()[0]
#     conn.close()
#     return count

# def delete_table():
#     conn = sqlite3.connect('data/database.db')
#     c = conn.cursor()
#     c.execute('DROP TABLE IF EXISTS tracking_data')
#     conn.commit()
#     conn.close()

# def read_table():
#     conn = sqlite3.connect('data/database.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM tracking_data')
#     rows = c.fetchall()
#     conn.close()
#     return rows

# def peoplecounter():
#     model = YOLO('yolov10n.pt')

#     area1 = [(415, 258), (553, 258), (553, 266), (415, 266)]
#     area2 = [(415, 286), (553, 286), (553, 274), (415, 274)]

#     initialize_db()

#     def process_video(video_source):
#         cap = cv2.VideoCapture(video_source)

#         with open("coco.txt", "r") as file:
#             class_list = file.read().split("\n")

#         tracker = Tracker()
#         people_in_area1 = set()
#         people_in_area2 = set()
#         person_area_status = {}

#         frame_window = st.image([])

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             frame = cv2.resize(frame, (1100, 400))
#             results = model.predict(frame)
#             a = results[0].boxes.data
#             px = pd.DataFrame(a).astype("float")
#             detected_people = []

#             for index, row in px.iterrows():
#                 x1 = int(row[0])
#                 y1 = int(row[1])
#                 x2 = int(row[2])
#                 y2 = int(row[3])
#                 d = int(row[5])
#                 c = class_list[d]
#                 if 'person' in c:
#                     detected_people.append([x1, y1, x2, y2])

#             bbox_id = tracker.update(detected_people)
#             current_area1 = set()
#             current_area2 = set()

#             for bbox in bbox_id:
#                 x3, y3, x4, y4, id = bbox
#                 in_area2 = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False) >= 0
#                 in_area1 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False) >= 0

#                 if in_area2:
#                     current_area2.add(id)
#                     cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
#                     cv2.putText(frame, f'In Area 2 {id}', (x3, y3 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)

#                 if in_area1:
#                     current_area1.add(id)
#                     cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
#                     cv2.putText(frame, f'In Area 1 {id}', (x3, y3 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)

#                 if id not in person_area_status:
#                     # Initial detection
#                     if in_area1:
#                         insert_entry(id, time.strftime('%Y-%m-%d %H:%M:%S'))
#                         person_area_status[id] = 'area1'
#                         people_in_area1.add(id)
#                     elif in_area2:
#                         insert_entry(id, time.strftime('%Y-%m-%d %H:%M:%S'))  # Mark as exit if detected in Area 2 first
#                         update_exit(id, time.strftime('%Y-%m-%d %H:%M:%S'))
#                         person_area_status[id] = 'area2'
#                         people_in_area2.add(id)
#                 else:
#                     last_area = person_area_status[id]
#                     if last_area == 'area1' and in_area2:
#                         update_exit(id, time.strftime('%Y-%m-%d %H:%M:%S'))
#                         people_in_area1.discard(id)
#                         people_in_area2.add(id)
#                         person_area_status[id] = 'area2'
#                     elif last_area == 'area2' and in_area1:
#                         insert_entry(id, time.strftime('%Y-%m-%d %H:%M:%S'))
#                         people_in_area2.discard(id)
#                         people_in_area1.add(id)
#                         person_area_status[id] = 'area1'

#             cv2.polylines(frame, [np.array(area1, np.int32)], True, (0, 0, 255))
#             cv2.putText(frame, 'Area 1', (467, 250), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

#             cv2.polylines(frame, [np.array(area2, np.int32)], True, (0, 0, 45))
#             cv2.putText(frame, 'Area 2', (467, 270), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

#             # Display the count of entries and exits
#             cv2.putText(frame, 'Total Enter:', (30, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
#             cv2.putText(frame, str(get_count('EnteringTime IS NOT NULL AND ExitingTime IS NULL')), (230, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

#             cv2.putText(frame, 'Total Exit:', (30, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
#             cv2.putText(frame, str(get_count('ExitingTime IS NOT NULL')), (230, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
            
#             camera, _ = st.columns([4, 2])
#             with camera:
#                 frame_window.image(frame, channels="BGR")

#         cap.release()
        
#     st.title("People Counting Application")

#     option = st.radio("Select Video Source", ("Upload Video", "Live Camera"))

#     if option == "Upload Video":
#         uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
#         if uploaded_video is not None:
#             with open("uploaded_video.mp4", "wb") as f:
#                 f.write(uploaded_video.getbuffer())
#             process_video("uploaded_video.mp4")

#     elif option == "Live Camera":
#         process_video(1)

#     st.title("Database Operations")
#     if st.button("Delete Table"):
#         delete_table()
#         st.success("Table deleted successfully.")

#     if st.button("Read Table"):
#         try:
#             rows = read_table()
#             if rows:
#                 st.dataframe(pd.DataFrame(rows, columns=["ID", "EnteringTime", "ExitingTime"]),
#                              use_container_width=True)
#             else:
#                 st.write("No data available in the table.")
#         except Exception as e:
#             st.write(f"Error: {str(e)}")
# peoplecounter()
from src.tracker import Tracker
from ultralytics import YOLO
import streamlit as st
import pandas as pd
import numpy as np
import time
import cv2
import sqlite3

def initialize_db():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tracking_data (
            ID INTEGER PRIMARY KEY,
            EnteringTime TEXT,
            ExitingTime TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_entry(id, entering_time):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO tracking_data (ID, EnteringTime, ExitingTime)
        VALUES (?, ?, ?)
    ''', (id, entering_time, None))
    conn.commit()
    conn.close()

def update_exit(id, exiting_time):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE tracking_data
        SET ExitingTime = ?
        WHERE ID = ? AND ExitingTime IS NULL
    ''', (exiting_time, id))
    conn.commit()
    conn.close()

def get_count(condition):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute(f'SELECT COUNT(*) FROM tracking_data WHERE {condition}')
    count = c.fetchone()[0]
    conn.close()
    return count

def delete_table():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS tracking_data')
    conn.commit()
    conn.close()

def read_table():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tracking_data')
    rows = c.fetchall()
    conn.close()
    return rows

def peoplecounter():
    model = YOLO('yolov10n.pt')

    area1 = [(415, 258), (553, 258), (553, 266), (415, 266)]
    area2 = [(415, 286), (553, 286), (553, 274), (415, 274)]

    initialize_db()

    def process_video(video_source):
        cap = cv2.VideoCapture(video_source)

        with open("coco.txt", "r") as file:
            class_list = file.read().split("\n")

        tracker = Tracker()
        people_in_area1 = set()
        people_in_area2 = set()
        person_area_status = {}

        frame_window = st.image([])

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (1100, 400))
            results = model.predict(frame)
            a = results[0].boxes.data
            px = pd.DataFrame(a).astype("float")
            detected_people = []

            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = class_list[d]
                if 'person' in c:
                    detected_people.append([x1, y1, x2, y2])

            bbox_id = tracker.update(detected_people)
            current_area1 = set()
            current_area2 = set()

            for bbox in bbox_id:
                x3, y3, x4, y4, id = bbox
                in_area2 = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False) >= 0
                in_area1 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False) >= 0

                if in_area2:
                    current_area2.add(id)
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    cv2.putText(frame, f'In Area 2 {id}', (x3, y3 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)

                if in_area1:
                    current_area1.add(id)
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                    cv2.putText(frame, f'In Area 1 {id}', (x3, y3 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)

                if id not in person_area_status:
                    # Initial detection
                    if in_area1:
                        insert_entry(id, time.strftime('%Y-%m-%d %H:%M:%S'))  # Mark as entering if detected in Area 1 first
                        person_area_status[id] = 'area1'
                        people_in_area1.add(id)
                    elif in_area2:
                        insert_entry(id, time.strftime('%Y-%m-%d %H:%M:%S'))  # Mark as entering if detected in Area 2 first
                        update_exit(id, time.strftime('%Y-%m-%d %H:%M:%S'))  # Mark as exiting immediately since it's an exit point
                        person_area_status[id] = 'area2'
                        people_in_area2.add(id)
                else:
                    last_area = person_area_status[id]
                    if last_area == 'area2' and in_area1:
                        update_exit(id, time.strftime('%Y-%m-%d %H:%M:%S'))
                        people_in_area2.discard(id)
                        people_in_area1.add(id)
                        person_area_status[id] = 'area1'
                    elif last_area == 'area1' and in_area2:
                        insert_entry(id, time.strftime('%Y-%m-%d %H:%M:%S'))
                        people_in_area1.discard(id)
                        people_in_area2.add(id)
                        person_area_status[id] = 'area2'

            cv2.polylines(frame, [np.array(area1, np.int32)], True, (0, 0, 255))
            cv2.putText(frame, 'Area 1', (467, 250), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

            cv2.polylines(frame, [np.array(area2, np.int32)], True, (0, 0, 45))
            cv2.putText(frame, 'Area 2', (467, 270), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

            # Display the count of entries and exits
            cv2.putText(frame, 'Total Enter:', (30, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, str(get_count('EnteringTime IS NOT NULL AND ExitingTime IS NULL')), (230, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

            cv2.putText(frame, 'Total Exit:', (30, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(frame, str(get_count('ExitingTime IS NOT NULL')), (230, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
            
            camera, _ = st.columns([4, 2])
            with camera:
                frame_window.image(frame, channels="BGR")

        cap.release()
        
    st.title("People Counting Application")

    option = st.radio("Select Video Source", ("Upload Video", "Live Camera"))

    if option == "Upload Video":
        uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
        if uploaded_video is not None:
            with open("uploaded_video.mp4", "wb") as f:
                f.write(uploaded_video.getbuffer())
            process_video("uploaded_video.mp4")

    elif option == "Live Camera":
        process_video(1)

    st.title("Database Operations")
    if st.button("Delete Table"):
        delete_table()
        st.success("Table deleted successfully.")

    if st.button("Read Table"):
        try:
            rows = read_table()
            if rows:
                st.dataframe(pd.DataFrame(rows, columns=["ID", "EnteringTime", "ExitingTime"]),
                             use_container_width=True)
            else:
                st.write("No data available in the table.")
        except Exception as e:
            st.write(f"Error: {str(e)}")

