import numpy as np
import argparse
import imutils
import sys
import cv2

# Argument parsing
argv = argparse.ArgumentParser()
argv.add_argument("-m", "--model", required=True, help="Path to pre-trained model")
argv.add_argument("-c", "--classes", required=True, help="Path to class labels file")
argv.add_argument("-i", "--input", type=str, default="", help="Path to input video file")
argv.add_argument("-o", "--output", type=str, default="", help="Path to output video file")
argv.add_argument("-g", "--gpu", type=int, default=0, help="Whether to use GPU or not")
args = vars(argv.parse_args())

# Load class labels
try:
    ACT = open(args["classes"]).read().strip().split("\n")
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)

# Constants
SAMPLE_DURATION = 16
SAMPLE_SIZE = 100       

print("Loading the Deep Learning Model for Human Activity Recognition")
gp = cv2.dnn.readNet(args["model"])

# Set GPU backend if requested
if args["gpu"] > 0:
    print("Setting preferable backend and target to CUDA...")
    gp.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    gp.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

print("Accessing the video stream...")
vs = cv2.VideoCapture(args["input"] if args["input"] else 0)

if not vs.isOpened():
    print("Error: Cannot open video stream.")
    sys.exit(1)

writer = None
fps = vs.get(cv2.CAP_PROP_FPS) 
print("Original FPS:", fps)

while True:
    frames = []
    originals = []

    for i in range(SAMPLE_DURATION):
        grabbed, frame = vs.read()
        if not grabbed:
            print("[INFO] No frame read from the stream - Exiting...")
            break
        originals.append(frame)
        frame = imutils.resize(frame, width=800)
        frames.append(frame)

    if not frames:
        break

    # Prepare input blob and perform inference
    blob = cv2.dnn.blobFromImages(frames, 1.0, (SAMPLE_SIZE, SAMPLE_SIZE), (114.7748, 107.7354, 99.4750), swapRB=True, crop=True)
    blob = np.transpose(blob, (1, 0, 2, 3))
    blob = np.expand_dims(blob, axis=0)

    gp.setInput(blob)
    outputs = gp.forward()
    label = ACT[np.argmax(outputs)]

    # Draw label on frames and save
    for frame in originals:
        cv2.rectangle(frame, (0, 0), (300, 40), (0, 0, 0), -1)
        cv2.putText(frame, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        if args["output"] != "" and writer is None:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(args["output"], fourcc, fps, (frame.shape[1], frame.shape[0]), True)

        if writer is not None:
            writer.write(frame)

# Release resources
vs.release()
if writer is not None:
    writer.release()
cv2.destroyAllWindows()
