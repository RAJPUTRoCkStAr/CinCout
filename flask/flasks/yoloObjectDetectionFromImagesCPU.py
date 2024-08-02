import cv2
import numpy as np

# Load YOLO
yolo = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Load the COCO class labels
classes = []
with open("coco.names", "r") as file:
    classes = [line.strip() for line in file.readlines()]

# Get the output layer names
layer_names = yolo.getLayerNames()
unconnected_layers = yolo.getUnconnectedOutLayers()

# Check the shape and type of unconnected_layers
if isinstance(unconnected_layers, np.ndarray) and len(unconnected_layers.shape) == 2:
    output_layers = [layer_names[i[0] - 1] for i in unconnected_layers]
else:
    output_layers = [layer_names[i - 1] for i in unconnected_layers]

# Colors for bounding boxes
colorRed = (0, 0, 255)
colorGreen = (0, 255, 0)

# Load image
name = "reading.jpg"
img = cv2.imread(name)
height, width, channels = img.shape

# Detect objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
yolo.setInput(blob)
outputs = yolo.forward(output_layers)

class_ids = []
confidences = []
boxes = []
for output in outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        cv2.rectangle(img, (x, y), (x + w, y + h), colorGreen, 3)
        cv2.putText(img, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, colorRed, 3)

# Save the output image
cv2.imwrite("output.jpg", img)
