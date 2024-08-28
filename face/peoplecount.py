import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from src.tracker import Tracker
import streamlit as st

def peoplecounter():
    model = YOLO('yolov10n.pt')


    area1 = [(600, 288), (574, 290), (770, 369), (782, 362)]
    area2 = [(564, 292), (535, 297), (708, 377), (760, 369)]

    def process_video(video_source):
        cap = cv2.VideoCapture(video_source)


        with open("coco.txt", "r") as my_file:
            data = my_file.read()
        class_list = data.split("\n")

        tracker = Tracker()
        people_entering = set()
        people_exiting = set()
        count = 0

        frame_window = st.image([])  

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            count += 1
            if count % 2 != 0:
                continue


            frame = cv2.resize(frame, (1100, 400))


            results = model.predict(frame)
            a = results[0].boxes.data
            px = pd.DataFrame(a).astype("float")

            bbox_list = []
            for _, row in px.iterrows():
                x1, y1, x2, y2, d = int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[5])
                c = class_list[d]
                if 'person' in c:
                    bbox_list.append([x1, y1, x2, y2])

            bbox_id = tracker.update(bbox_list)
            for bbox in bbox_id:
                x3, y3, x4, y4, id = bbox

                if cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False) >= 0:
                    people_entering.add(id)
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)

                if id in people_entering and cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False) >= 0:
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    cv2.circle(frame, (x2, y2), 4, (0, 255, 0), -1)
                    cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

                if cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False) >= 0:
                    people_exiting.add(id)
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)

                if id in people_exiting and cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False) >= 0:
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    cv2.circle(frame, (x2, y2), 4, (255, 0, 255), -1)
                    cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

            cv2.polylines(frame, [np.array(area1, np.int32)], True, (255, 255, 255))
            cv2.putText(frame, 'area1', (504, 471), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
            cv2.polylines(frame, [np.array(area2, np.int32)], True, (255, 255, 255))
            cv2.putText(frame, 'area2', (466, 485), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

            enter_count = len(people_entering)
            exit_count = len(people_exiting)
            cv2.putText(frame, 'Total Enter Person', (30, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, str(enter_count), (270, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, 'Total Exit Person', (30, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
            cv2.putText(frame, str(exit_count), (250, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)

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
        process_video(0)  
