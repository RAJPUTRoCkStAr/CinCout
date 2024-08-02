
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import datetime  # Import the datetime module

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Replace the connection string with your MongoDB URI
client = MongoClient('mongodb://localhost:27017')
db = client['Human']  # Replace with your database name
signup_collection = db['signup']
login_collection = db['login']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'signup' in request.form:
            return redirect(url_for('signup'))
        elif 'login' in request.form:
            return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = signup_collection.find_one({'username': username})
        if existing_user:
            return "User already exists! Please log in."

        signup_collection.insert_one({
            'username': username,
            'email': email,
            'password': password  # Storing plain text password (Not recommended for production)
        })
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Corrected condition
        username = request.form['username']
        password = request.form['password']

        user = signup_collection.find_one({'username': username})
        if user and user['password'] == password:
            login_collection.insert_one({
                'username': username,
                'login_time': datetime.datetime.now()  # Log the login time
            })
            session['username'] = username
            return redirect(url_for('main'))
        return "Invalid credentials! Please try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
# from pymongo import MongoClient
# import datetime
# import os
# import cv2
# import numpy as np
# from werkzeug.utils import secure_filename

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# # MongoDB setup
# client = MongoClient('mongodb://localhost:27017')
# db = client['Human']
# signup_collection = db['signup']
# login_collection = db['login']

# # YOLO setup
# yolo = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# classes = []
# with open("coco.names", "r") as file:
#     classes = [line.strip() for line in file.readlines()]

# layer_names = yolo.getLayerNames()
# unconnected_layers = yolo.getUnconnectedOutLayers()
# if isinstance(unconnected_layers, np.ndarray) and len(unconnected_layers.shape) == 2:
#     output_layers = [layer_names[i[0] - 1] for i in unconnected_layers]
# else:
#     output_layers = [layer_names[i - 1] for i in unconnected_layers]

# UPLOAD_FOLDER = 'uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# def detect_objects(image_path):
#     img = cv2.imread(image_path)
#     height, width, channels = img.shape
#     blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#     yolo.setInput(blob)
#     outputs = yolo.forward(output_layers)
#     class_ids, confidences, boxes = [], [], []

#     for output in outputs:
#         for detection in output:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if confidence > 0.5:
#                 center_x, center_y = int(detection[0] * width), int(detection[1] * height)
#                 w, h = int(detection[2] * width), int(detection[3] * height)
#                 x, y = int(center_x - w / 2), int(center_y - h / 2)
#                 boxes.append([x, y, w, h])
#                 confidences.append(float(confidence))
#                 class_ids.append(class_id)

#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#     for i in range(len(boxes)):
#         if i in indexes:
#             x, y, w, h = boxes[i]
#             label = str(classes[class_ids[i]])
#             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
#             cv2.putText(img, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

#     output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.jpg')
#     cv2.imwrite(output_path, img)
#     return output_path

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'signup' in request.form:
#             return redirect(url_for('signup'))
#         elif 'login' in request.form:
#             return redirect(url_for('login'))
#     return render_template('index.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username, email, password = request.form['username'], request.form['email'], request.form['password']
#         if signup_collection.find_one({'username': username}):
#             return "User already exists! Please log in."
#         signup_collection.insert_one({'username': username, 'email': email, 'password': password})
#         return redirect(url_for('login'))
#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username, password = request.form['username'], request.form['password']
#         user = signup_collection.find_one({'username': username})
#         if user and user['password'] == password:
#             login_collection.insert_one({'username': username, 'login_time': datetime.datetime.now()})
#             session['username'] = username
#             return redirect(url_for('main'))
#         return "Invalid credentials! Please try again."
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('index'))

# @app.route('/main', methods=['GET', 'POST'])
# def main():
#     if 'username' in session:
#         if request.method == 'POST':
#             file = request.files['file']
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(file_path)
#                 output_path = detect_objects(file_path)
#                 return render_template('main.html', filename='output.jpg')
#         return render_template('main.html')
#     return redirect(url_for('login'))

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# if __name__ == '__main__':
#     if not os.path.exists(app.config['UPLOAD_FOLDER']):
#         os.makedirs(app.config['UPLOAD_FOLDER'])
#     app.run(debug=True)
