#python Videos.py --model resnet-34_kinetics.onnx --classes Actions.txt --input media/boxing.mp4 --output output.mp4 --gpu 1 --yolo-cfg yolov3.cfg --yolo-weights yolov3.weights --yolo-classes coco.names
#python Videos.py --model resnet-34_kinetics.onnx --classes Actions.txt --yolo-cfg yolov3.cfg --yolo-weights yolov3.weights --yolo-classes coco.names



import numpy as np
import argparse
import imutils
import sys
import cv2
import os

# Create argument parser
argv = argparse.ArgumentParser()
argv.add_argument("-m", "--model", required=True, help="Path to pre-trained model")
argv.add_argument("-c", "--classes", required=True, help="Path to class labels file")
argv.add_argument("-i", "--input", type=str, default="", help="Path to input video file")
argv.add_argument("-o", "--output", type=str, default="", help="Path to output video file")
argv.add_argument("-d", "--display", type=int, default=1, help="Whether to display output frame or not")
argv.add_argument("-g", "--gpu", type=int, default=0, help="Whether to use GPU or not")
argv.add_argument("--yolo-cfg", required=True, help="Path to YOLO config file")
argv.add_argument("--yolo-weights", required=True, help="Path to YOLO weights file")
argv.add_argument("--yolo-classes", required=True, help="Path to YOLO classes file")
args = vars(argv.parse_args())

# Load the class labels(action.txt) file
try:
    ACT = open(args["classes"]).read().strip().split("\n")
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)

SAMPLE_DURATION = 16
SAMPLE_SIZE = 100       

# Load the Deep Learning model for activity recognition
print("Loading the Deep Learning Model for Human Activity Recognition")
gp = cv2.dnn.readNet(args["model"])

# Load the YOLO model for person detection
print("Loading YOLO model for person detection")
yolo_net = cv2.dnn.readNet(args["yolo_weights"], args["yolo_cfg"])
if args["gpu"] > 0:
    print("Setting preferable backend and target to CUDA for YOLO...")
    yolo_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    yolo_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Load COCO class labels for YOLO
try:
    yolo_classes = open(args["yolo_classes"]).read().strip().split("\n")
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)

# Get the output layer names for YOLO
yolo_layer_names = yolo_net.getUnconnectedOutLayersNames()

# Check if GPU will be used for activity recognition
if args["gpu"] > 0:
    print("Setting preferable backend and target to CUDA for Activity Recognition...")
    gp.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    gp.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Access the video stream
print("Accessing the video stream...")
vs = cv2.VideoCapture(args["input"] if args["input"] else 0)
writer = None
fps = vs.get(cv2.CAP_PROP_FPS) 
print("Original FPS:", fps)

# Process video frames
while True:
    frames = []
    originals = []

    # Sample frames
    for i in range(SAMPLE_DURATION):
        (grabbed, frame) = vs.read()
        if not grabbed:
            print("[INFO] No frame read from the stream - Exiting...")
            sys.exit(0)
        originals.append(frame)
        frame = imutils.resize(frame, width=400)
        frames.append(frame)

    # Construct blob for activity recognition
    blob = cv2.dnn.blobFromImages(frames, 1.0, (SAMPLE_SIZE, SAMPLE_SIZE), (114.7748, 107.7354, 99.4750), swapRB=True, crop=True)
    blob = np.transpose(blob, (1, 0, 2, 3))
    blob = np.expand_dims(blob, axis=0)

    # Predict activity
    gp.setInput(blob)
    outputs = gp.forward()
    label = ACT[np.argmax(outputs)]

    # Add labels to frames and detect persons using YOLO
    for frame in originals:
        # Prepare the frame for YOLO
        yolo_blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        yolo_net.setInput(yolo_blob)
        yolo_outputs = yolo_net.forward(yolo_layer_names)
        
        boxes = []
        confidences = []
        classIDs = []
        
        for output in yolo_outputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if classID == yolo_classes.index("person") and confidence > 0.5:
                    box = detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        
        # Apply non-maxima suppression
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
        
        # Draw bounding boxes and labels
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = f"{yolo_classes[classIDs[i]]}: {confidences[i]:.4f}"
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Add activity label
        cv2.rectangle(frame, (0, 0), (300, 40), (0, 0, 0), -1)
        cv2.putText(frame, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Display frame
        if args["display"] > 0:
            cv2.imshow("Activity Recognition", frame)
            key = cv2.waitKey(10) & 0xFF
            if key == ord("q"):
                break

        # Initialize video writer if needed
        if args["output"] != "" and writer is None:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(args["output"], fourcc, fps, (frame.shape[1], frame.shape[0]), True)

        # Write frame to output
        if writer is not None:
            writer.write(frame)
vs.release()
if writer is not None:
    writer.release()
cv2.destroyAllWindows()


