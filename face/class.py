from ultralytics import YOLO

# Load a pre-trained YOLOv8 model
model = YOLO('testing/yolov10n.pt')
print(model.names)