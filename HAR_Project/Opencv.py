# USAGE
# python human_activity_recognition_deque.py --model resnet-34_kinetics.onnx --classes action_recognition_kinetics.txt --input videos/example_activities.mp4
# python human_activity_recognition_deque.py --model resnet-34_kinetics.onnx --classes action_recognition_kinetics.txt

# Import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import onnxruntime as ort

# Argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="path to trained human activity recognition model")
ap.add_argument("-c", "--classes", required=True, help="path to class labels file")
ap.add_argument("-i", "--input", type=str, default="", help="optional path to video file")
args = vars(ap.parse_args())

# Load class labels
CLASSES = open(args["classes"]).read().strip().split("\n")

# Constants
SAMPLE_DURATION = 16
SAMPLE_SIZE = 112

# Initialize frame queue
frames = deque(maxlen=SAMPLE_DURATION)

# Load the human activity recognition model using ONNX Runtime
print("[INFO] Loading the human activity recognition model...")
try:
    session = ort.InferenceSession(args["model"])
    print("[INFO] Model loaded successfully.")
except Exception as e:
    print(f"[ERROR] Failed to load the model: {e}")
    exit(1)

# Access the video stream
print("[INFO] Accessing the video stream...")
vs = cv2.VideoCapture(args["input"] if args["input"] else 0)

# Frame processing interval
frame_interval = 2
frame_count = 0

while True:
    (grabbed, frame) = vs.read()
    if not grabbed:
        print("[INFO] No frame read from the video stream - Exiting...")
        break

    frame_count += 1
    if frame_count % frame_interval != 0:
        continue

    frame = imutils.resize(frame, width=SAMPLE_SIZE)
    frame = cv2.flip(frame, 1)
    frames.append(frame)

    if len(frames) < SAMPLE_DURATION:
        continue

    blob = cv2.dnn.blobFromImages(frames, 1.0, (SAMPLE_SIZE, SAMPLE_SIZE), (114.7748, 107.7354, 99.4750),
                                  swapRB=True, crop=True)
    blob = np.transpose(blob, (1, 0, 2, 3))
    blob = np.expand_dims(blob, axis=0)
    inputs = {session.get_inputs()[0].name: blob}
    outputs = session.run(None, inputs)[0]
    label = CLASSES[np.argmax(outputs)]

    cv2.rectangle(frame, (0, 0), (300, 40), (0, 0, 0), -1)
    cv2.putText(frame, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Activity Recognition", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release the video stream and close windows
vs.release()
cv2.destroyAllWindows()
