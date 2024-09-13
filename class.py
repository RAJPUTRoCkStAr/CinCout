# from ultralytics import YOLO

# # Load a pre-trained YOLOv8 model
# model = YOLO('testing/yolov10n.pt')
# print(model.names)
import cv2
from ultralytics import YOLO

print("OpenCV version:", cv2.__version__)
print("Ultralytics YOLO version:", YOLO._version__)
