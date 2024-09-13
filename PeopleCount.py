import cv2
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
from ultralytics import YOLO
from src.tracker import Tracker
import sqlite3
from datetime import datetime


conn = sqlite3.connect('Data/database.db', check_same_thread=False)
db_cursor = conn.cursor()

db_cursor.execute('''
CREATE TABLE IF NOT EXISTS person_log (
    person_id INTEGER,
    status TEXT,
    timestamp TEXT
)
''')
conn.commit()


def log_person_entry_exit(person_id, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_cursor.execute("INSERT INTO person_log (person_id, status, timestamp) VALUES (?, ?, ?)", (person_id, status, timestamp))
    conn.commit()


def view_log():
    db_cursor.execute("SELECT * FROM person_log")
    data = db_cursor.fetchall()
    df = pd.DataFrame(data, columns=["person_id", "status", "timestamp"])
    return df


def delete_row(person_id):
    db_cursor.execute("DELETE FROM person_log WHERE person_id = ?", (person_id,))
    conn.commit()
    st.success(f"Deleted person with ID {person_id}")

def peoplecounter():
    
    model = YOLO('yolov10n.pt')

    # Define the areas for entry and exit detection (top-left, top-right, bottom-right, bottom-left corners)
    area1 = [(365, 256), (603, 256), (603, 268), (365, 268)]
    area2 = [(365, 288), (603, 288), (603, 272), (365, 272)]

    with open("coco.txt", "r") as my_file:
        data = my_file.read()
    class_list = data.split("\n")


    tracker = Tracker()
    people_entering = {}
    entering = set()
    people_exiting = {}
    exiting = set()


    # st.title("Person Counting and Log Viewer")
    st.markdown(f"<h2 style='text-align: center;color:white'>Person Counting and Log Viewer</h2>", unsafe_allow_html=True)
    add = option_menu(
    "Main Menu",
    ["People Counter", "View/Delete Logs"], 
   icons = [
    'person-standing',              # People Counter
    'file-earmark-text'             # View/Delete Logs
    ], 
    menu_icon="menu-up", 
    default_index=0,orientation="horizontal"
)
    # tab1, tab2 = st.tabs(["People Counter", "View/Delete Logs"])
    if add == 'People Counter':
        use_camera = st.checkbox("Use Live Camera")
        cap = None
        if use_camera:
            cap = cv2.VideoCapture(0)
            st.success('Successfully opened live camera!')
        else:
            st.info("You are not using camera !")
            # uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "avi", "mov"])
            # if uploaded_video is not None:
            #     video_bytes = uploaded_video.read()
            #     cap = cv2.VideoCapture(cv2.VideoCapture(cv2.imdecode(np.frombuffer(video_bytes, np.uint8), cv2.IMREAD_COLOR)))
            #     st.success('Successfully uploaded video!')
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

          
                frame = cv2.resize(frame, (900, 330))

 
                results = model.predict(frame)

      
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

           
                bbox_id = tracker.update(list_of_boxes)

                for bbox in bbox_id:
                    x3, y3, x4, y4, person_id = bbox
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

           
                cv2.polylines(frame, [np.array(area1, np.int32)], True, (255, 255, 255))
                cv2.putText(frame, 'area1', (504, 471), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.polylines(frame, [np.array(area2, np.int32)], True, (255, 255, 255))
                cv2.putText(frame, 'area2', (466, 485), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

   
                Enter = len(entering)
                Exit = len(exiting)

                cv2.putText(frame, 'Total Enter Person', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
                cv2.putText(frame, str(Enter), (210, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
                cv2.putText(frame, 'Total Exit Person', (30, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 1)
                cv2.putText(frame, str(Exit), (200, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 1)


                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, f'{current_time}', (680, 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)

          
                stframe.image(frame, channels="BGR", use_column_width=True)

            cap.release()

    if add == 'View/Delete Logs':
        # st.header("View and Delete Person Logs")
        st.markdown(f"<h2 style='text-align: center;color:white'>View People Count</h2>", unsafe_allow_html=True)
        df = view_log()
        st.dataframe(df,use_container_width=True,hide_index=True,)
        st.markdown(f"<h2 style='text-align: center;color:white'>Delete People Count by Person ID</h2>", unsafe_allow_html=True)
        person_id_to_delete = st.number_input("Enter Person ID to delete", min_value=0, step=1)
        if st.button("Delete Row"):
            delete_row(person_id_to_delete)
            
            df = view_log()
            st.dataframe(df,use_container_width=True,hide_index=True)

if __name__ == "__main__":
    peoplecounter()
