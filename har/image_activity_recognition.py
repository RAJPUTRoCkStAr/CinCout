import numpy as np
import argparse
import cv2
import sys

# Argument parsing
argv = argparse.ArgumentParser()
argv.add_argument("-m", "--model", required=True, help="Path to pre-trained model")
argv.add_argument("-c", "--classes", required=True, help="Path to class labels file")
argv.add_argument("-i", "--input", required=True, help="Path to input image file")
argv.add_argument("-o", "--output", type=str, default="", help="Path to output image file")
argv.add_argument("-d", "--display", type=int, default=1, help="Whether to display output image or not")
argv.add_argument("-g", "--gpu", type=int, default=0, help="Whether to use GPU or not")
args = vars(argv.parse_args())

# Load class labels
try:
    ACT = open(args["classes"]).read().strip().split("\n")
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)

# Load the Deep Learning Model
print("Loading the Deep Learning Model for Human Activity Recognition")
gp = cv2.dnn.readNet(args["model"])

if args["gpu"] > 0:
    print("Setting preferable backend and target to CUDA...")
    gp.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    gp.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Read the input image
print("Loading the input image...")
image = cv2.imread(args["input"] if args["input"] else 0)
if image is None:
    print(f"Error: Could not read the image file: {args['input']}")
    sys.exit(1)
SAMPLE_SIZE = 100  
# Resize image if necessary (depends on your model's requirements)
image_resized = cv2.resize(image, (SAMPLE_SIZE, SAMPLE_SIZE))

# Prepare image blob
blob = cv2.dnn.blobFromImages(image_resized, 1.0, (SAMPLE_SIZE, SAMPLE_SIZE), (114.7748, 107.7354, 99.4750), swapRB=True, crop=True)
blob = np.transpose(blob, (1, 0, 2, 3))
blob = np.expand_dims(blob, axis=0)

# Perform inference
gp.setInput(blob)
outputs = gp.forward()
label = ACT[np.argmax(outputs)]

# Draw label on image
cv2.rectangle(image, (0, 0), (300, 40), (0, 0, 0), -1)
cv2.putText(image, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

# Display or save output
if args["display"] > 0:
    cv2.imshow("Activity Recognition", image)
    cv2.waitKey(0)  # Wait indefinitely until a key is pressed
    cv2.destroyAllWindows()

if args["output"] != "":
    cv2.imwrite(args["output"], image)

print("Processing complete.")


