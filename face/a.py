# import cv2
# import pandas as pd
# import numpy as np
# from ultralytics import YOLO
# from src.tracker import *
# import time

# model = YOLO('yolov8s.pt')

# # Define areas
# area1 = [(415, 258), (553, 258), (553, 266), (415, 266)]
# area2 = [(415, 286), (553, 286), (553, 274), (415, 274)]

# # Function to detect mouse position (for debugging)
# def RGB(event, x, y, flags, param):
#     if event == cv2.EVENT_MOUSEMOVE:  
#         colorsBGR = [x, y]
#         print(colorsBGR)
        
# cv2.namedWindow('RGB')
# cv2.setMouseCallback('RGB', RGB)

# cap = cv2.VideoCapture(1)

# # Load class list
# with open("coco.txt", "r") as file:
#     class_list = file.read().split("\n")

# tracker = Tracker()
# people_in_area1 = set()
# people_in_area2 = set()
# entering = {}
# exiting = {}

# while True:    
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.resize(frame, (1100, 400))
#     results = model.predict(frame)
#     a = results[0].boxes.data
#     px = pd.DataFrame(a).astype("float")
#     detected_people = []
             
#     for index, row in px.iterrows():
#         x1 = int(row[0])
#         y1 = int(row[1])
#         x2 = int(row[2])
#         y2 = int(row[3])
#         d = int(row[5])
#         c = class_list[d]
#         if 'person' in c:
#             detected_people.append([x1, y1, x2, y2])

#     bbox_id = tracker.update(detected_people)
    
#     # Create a copy of current area tracking states
#     current_area1 = set()
#     current_area2 = set()

#     for bbox in bbox_id:
#         x3, y3, x4, y4, id = bbox
#         results = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
        
#         # Check if the person is in area2
#         in_area2 = results >= 0
#         if in_area2:
#             current_area2.add(id)
#             cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
        
#         results1 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
#         # Check if the person is also in area1
#         in_area1 = results1 >= 0
#         if in_area1:
#             current_area1.add(id)
#             cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)

#         # Track transitions from area2 to area1
#         if id in people_in_area2 and id not in current_area2:
#             if id not in exiting:
#                 exiting[id] = time.strftime('%Y-%m-%d %H:%M:%S')
#             cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
#             cv2.circle(frame, (x2, y2), 4, (0, 0, 255), -1)
#             cv2.putText(frame, f'Exiting {id}', (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
#             people_in_area2.remove(id)

#         # Track transitions from area1 to area2
#         if id in people_in_area1 and id not in current_area1:
#             if id not in entering:
#                 entering[id] = time.strftime('%Y-%m-%d %H:%M:%S')
#             cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
#             cv2.circle(frame, (x2, y2), 4, (0, 255, 0), -1)
#             cv2.putText(frame, f'Entering {id}', (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)
#             people_in_area1.remove(id)

#     # Update people in area lists
#     people_in_area1.update(current_area1)
#     people_in_area2.update(current_area2)

#     # Draw areas on the frame
#     cv2.polylines(frame, [np.array(area1, np.int32)], True, (0, 0, 255))
#     cv2.putText(frame, 'Area 1', (467, 250), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
    
#     cv2.polylines(frame, [np.array(area2, np.int32)], True, (0, 0, 45))
#     cv2.putText(frame, 'Area 2', (467, 270), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

#     # Print counts and timestamps in the terminal
#     Enter = len(entering)
#     Exit = len(exiting)
    
#     print(f'Total Enter Person: {Enter}')
#     for pid, time_str in entering.items():
#         print(f'ID {pid} Entered at: {time_str}')
    
#     print(f'Total Exit Person: {Exit}')
#     for pid, time_str in exiting.items():
#         print(f'ID {pid} Exited at: {time_str}')
    
#     # Show counts on the frame
#     cv2.putText(frame, 'Total Exit:', (30, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
#     cv2.putText(frame, str(Exit), (230, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
    
#     cv2.putText(frame, 'Total Enter:', (30, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
#     cv2.putText(frame, str(Enter), (230, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
    
#     cv2.imshow("RGB", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from src.tracker import Tracker
import time

model = YOLO('yolov8s.pt')

# Define areas
area1 = [(415, 258), (553, 258), (553, 266), (415, 266)]
area2 = [(415, 286), (553, 286), (553, 274), (415, 274)]

# Function to detect mouse position (for debugging)
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture(1)

# Load class list
with open("coco.txt", "r") as file:
    class_list = file.read().split("\n")

tracker = Tracker()
people_in_area1 = set()
people_in_area2 = set()
entering = {}
exiting = {}
person_area_status = {}  # Track where each person was last seen

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
    
    # Create a copy of current area tracking states
    current_area1 = set()
    current_area2 = set()

    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        results = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
        in_area2 = results >= 0
        if in_area2:
            current_area2.add(id)
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
        
        results1 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
        in_area1 = results1 >= 0
        if in_area1:
            current_area1.add(id)
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)

        # Track transitions and update lists accordingly
        if id in person_area_status:
            last_area = person_area_status[id]
            
            # Transition from area2 to area1 (exiting)
            if id in people_in_area2 and id not in current_area2:
                if last_area == 'area2':
                    if id not in exiting:
                        exiting[id] = time.strftime('%Y-%m-%d %H:%M:%S')
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                    cv2.circle(frame, (x2, y2), 4, (0, 0, 255), -1)
                    cv2.putText(frame, f'Exiting {id}', (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                    people_in_area2.remove(id)
            
            # Transition from area1 to area2 (entering)
            if id in people_in_area1 and id not in current_area1:
                if last_area == 'area1':
                    if id not in entering:
                        entering[id] = time.strftime('%Y-%m-%d %H:%M:%S')
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    cv2.circle(frame, (x2, y2), 4, (0, 255, 0), -1)
                    cv2.putText(frame, f'Entering {id}', (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)
                    people_in_area1.remove(id)

        # Update the person_area_status based on current area
        if id in current_area1:
            person_area_status[id] = 'area1'
            people_in_area1.add(id)
        elif id in current_area2:
            person_area_status[id] = 'area2'
            people_in_area2.add(id)
        else:
            if id in person_area_status:
                del person_area_status[id]

    # Draw areas on the frame
    cv2.polylines(frame, [np.array(area1, np.int32)], True, (0, 0, 255))
    cv2.putText(frame, 'Area 1', (467, 250), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
    
    cv2.polylines(frame, [np.array(area2, np.int32)], True, (0, 0, 45))
    cv2.putText(frame, 'Area 2', (467, 270), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

    # Print counts and timestamps in the terminal
    Enter = len(entering)
    Exit = len(exiting)
    
    print(f'Total Enter Person: {Enter}')
    for pid, time_str in entering.items():
        print(f'ID {pid} Entered at: {time_str}')
    
    print(f'Total Exit Person: {Exit}')
    for pid, time_str in exiting.items():
        print(f'ID {pid} Exited at: {time_str}')
    
    # Show counts on the frame
    cv2.putText(frame, 'Total Exit:', (30, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, str(Exit), (230, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.putText(frame, 'Total Enter:', (30, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(frame, str(Enter), (230, 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
    
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
