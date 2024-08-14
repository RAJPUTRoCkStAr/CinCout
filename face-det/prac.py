import uuid
import streamlit as st
import os
import cv2
from streamlit_option_menu import option_menu
import shutil
import numpy as np
import pandas as pd
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import datetime
import sqlite3
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

# Constants and configurations
allowed_image_type = ['.png', 'jpg', '.jpeg']
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VISITOR_HISTORY = os.path.join(ROOT_DIR, "visitor_history")
COLOR_DARK = (0, 0, 153)
COLOR_WHITE = (255, 255, 255)
COLS_INFO = ['Name']
COLS_ENCODE = [f'v{i}' for i in range(512)]
DB_PATH = os.path.join(ROOT_DIR, "users.db")

# Initialize face recognition models
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20, thresholds=[0.6, 0.7, 0.7], factor=0.709, device=device, keep_all=True)

# Database initialization
def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS visitors (
        Unique_ID TEXT PRIMARY KEY,
        Name TEXT NOT NULL,
        Email TEXT NOT NULL,
        {', '.join(f'{col} REAL' for col in COLS_ENCODE)}
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        ID TEXT,
        visitor_name TEXT,
        Timing TEXT,
        Image_Path TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Database connection
def connect_db(db_path=DB_PATH):
    return sqlite3.connect(db_path)

# Helper functions
def generate_10_digit_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) + str(uuid.uuid4().int % 1000000).zfill(4)

def is_gmail(email):
    return email.lower().endswith('@gmail.com')

def is_email_registered(email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM visitors WHERE Email = ?", (email,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def add_data_db(visitor_details):
    conn = connect_db()
    cursor = conn.cursor()
    for _, row in visitor_details.iterrows():
        cursor.execute(f'''
        INSERT OR REPLACE INTO visitors (Unique_ID, Name, Email, {', '.join(COLS_ENCODE)})
        VALUES (?, ?, ?, {', '.join('?' * len(COLS_ENCODE))})
        ''', (row['Unique_ID'], row['Name'], row['Email'], *row[COLS_ENCODE]))
    conn.commit()
    conn.close()
    st.success('Details Added Successfully!')

def get_data_from_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM visitors')
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=['Unique_ID', 'Name'] + COLS_ENCODE)

def add_attendance(id, name):
    conn = connect_db()
    cursor = conn.cursor()
    dtString = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO attendance (ID, visitor_name, Timing, Image_Path) VALUES (?, ?, ?, ?)', 
                   (id, name, dtString, f'{id}.jpg'))
    conn.commit()
    conn.close()

def get_attendance_records():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM attendance')
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=['ID', 'visitor_name', 'Timing', 'Image_Path'])

def send_email(recipient_email, subject, body):
    sender_email = os.getenv('SMTP_USERNAME')
    sender_password = os.getenv('SMTP_PASSWORD')
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            st.success(f"Unique ID sent to {recipient_email}")
    except smtplib.SMTPException as e:
        st.error(f"SMTP error occurred: {str(e)}")

# Application functions
def view_attendance():
    st.write("### Attendance Records")
    df_combined = get_attendance_records()
    if df_combined.empty:
        st.warning("No attendance records found.")
        return
    df_combined.sort_values(by='Timing', ascending=False, inplace=True)
    df_combined.reset_index(drop=True, inplace=True)
    def encode_image(image_path):
        full_image_path = os.path.join(VISITOR_HISTORY, image_path)
        if image_path and os.path.isfile(full_image_path):
            with open(full_image_path, "rb") as image_file:
                return "data:image/jpeg;base64," + base64.b64encode(image_file.read()).decode()
        return None
    df_combined['image'] = df_combined['Image_Path'].apply(encode_image)
    try:
        st.data_editor(
            df_combined.drop(columns=["Image_Path"]),
            column_config={
                "ID": st.column_config.Column("ID"),
                "visitor_name": st.column_config.Column("Visitor Name"),
                "Timing": st.column_config.Column("Timing"),
                "image": st.column_config.ImageColumn("Visitor Image", help="Preview of visitor images")
            },
            hide_index=True,
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error displaying attendance data: {e}")

def Takeattendance():
    visitor_id = st.text_input("Enter your Unique ID:", '')
    if not visitor_id:
        st.error("Please enter your Unique ID.")
        return
    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        image_array = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        image_array_copy = image_array.copy()
        with open(os.path.join(VISITOR_HISTORY, f'{visitor_id}.jpg'), 'wb') as file:
            file.write(img_file_buffer.getbuffer())
            st.success('Image Saved Successfully!')
            boxes, probs = mtcnn.detect(image_array, landmarks=False)
            if boxes is not None:
                aligned = []
                for box in boxes:
                    face = image_array[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                    aligned_face = mtcnn(face)
                    if aligned_face is not None:
                        aligned.append(resnet(aligned_face.to(device)).detach().cpu())
                if len(aligned) > 0:
                    similarity_threshold = st.slider('Select Threshold for Similarity', min_value=0.0, max_value=3.0, value=0.5)
                    for face_idx, face_to_compare in enumerate(aligned):
                        database_data = get_data_from_db()
                        face_encodings = database_data[COLS_ENCODE].values
                        similarity = np.dot(face_encodings, face_to_compare.numpy().T)
                        if similarity.max() > similarity_threshold:
                            idx = np.argmax(similarity)
                            name_visitor = database_data.iloc[idx]['Name']
                            add_attendance(visitor_id, name_visitor)
                            (left, top, right, bottom) = map(int, boxes[face_idx])
                            cv2.rectangle(image_array_copy, (left, top), (right, bottom), COLOR_DARK, 2)
                            cv2.putText(image_array_copy, f"#{name_visitor}", (left + 5, bottom + 25), cv2.FONT_HERSHEY_DUPLEX, .55, COLOR_WHITE, 1)
                            st.image(image_array_copy, width=720)
                            st.success("Attendance Marked successfully")
                        else:
                            st.error('No Match Found for the given Similarity Threshold!')
                            add_attendance(visitor_id, 'Unknown')
            else:
                st.error('No human face detected.')

def personadder():
    face_name = st.text_input('Name:', '')
    email = st.text_input('Email:', '')
    pic_option = st.selectbox('Upload Picture', ["Upload your Profile Picture", "Take a Picture with Cam"])
    img_file_buffer = st.file_uploader('Upload a Picture', type=allowed_image_type) if pic_option == 'Upload your Profile Picture' else st.camera_input("Take a Picture with Cam")
    if img_file_buffer is not None:
        if ((len(face_name) > 1) & (len(email) > 1) & st.button('Click to Save!', use_container_width=True)):
            if not is_gmail(email):
                st.error("Please enter a valid Gmail address.")
                return
            if is_email_registered(email):
                st.error("This email is already registered. Please use a different email.")
                return
            unique_id = generate_10_digit_id()
            file_bytes = np.asarray(bytearray(img_file_buffer.read()), dtype=np.uint8) if pic_option == 'Upload your Profile Picture' else np.frombuffer(img_file_buffer.getvalue(), np.uint8)
            image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            if image_array is None:
                st.error("Error loading the image. Please try again.")
                return
            with open(os.path.join(ROOT_DIR, f'{face_name}_{unique_id}.jpg'), 'wb') as file:
                file.write(img_file_buffer.getbuffer())
            image_array_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            face_locations, _ = mtcnn(image_array_rgb, return_prob=True)
            if face_locations is None or len(face_locations) == 0:
                st.error("No faces detected in the image. Please try again.")
                st.write("Debugging Info:")
                st.write(f"Image shape: {image_array.shape}")
                st.write(f"Face locations: {face_locations}")
                return
            torch_loc = torch.stack([face_locations[0]]).to(device)
            encodesCurFrame = resnet(torch_loc).detach().cpu()
            df_new = pd.DataFrame(data=encodesCurFrame, columns=COLS_ENCODE)
            df_new['Name'] = face_name
            df_new['Unique_ID'] = unique_id
            df_new['Email'] = email
            df_new = df_new[['Unique_ID'] + ['Name'] + ['Email'] + COLS_ENCODE].copy()
            add_data_db(df_new)
            email_body = f"Hello {face_name},\n\nYour unique ID is: {unique_id}\n\nBest regards,\nTeam"
            send_email(email, "Your Unique ID", email_body)

def search_attendance():
    st.header("Search Attendance Records")
    search_type = st.selectbox("Search by", ["Visitor ID", "Name"])
    search_input = st.text_input(f"Enter {search_type} to search:", '')
    if search_input:
        df_combined = get_attendance_records()
        if search_type == "Visitor ID":
            search_results = df_combined[df_combined['ID'] == search_input]
        else:
            search_results = df_combined[df_combined['visitor_name'].str.contains(search_input, case=False, na=False)]
        if not search_results.empty:
            st.write("### Search Results")
            def encode_image(image_path):
                full_image_path = os.path.join(VISITOR_HISTORY, image_path)
                if os.path.isfile(full_image_path):
                    with open(full_image_path, "rb") as image_file:
                        return "data:image/jpeg;base64," + base64.b64encode(image_file.read()).decode()
                return None
            search_results['image'] = search_results['Image_Path'].apply(encode_image)
            try:
                st.data_editor(
                    search_results.drop(columns=["Image_Path"]),
                    column_config={
                        "ID": st.column_config.Column("ID"),
                        "visitor_name": st.column_config.Column("Visitor Name"),
                        "Timing": st.column_config.Column("Timing"),
                        "image": st.column_config.ImageColumn("Visitor Image", help="Preview of visitor images")
                    },
                    hide_index=True,
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error displaying search results: {e}")
        else:
            st.warning(f"No records found for {search_type}: {search_input}")

def cleardatabase():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM visitors")
    conn.commit()
    conn.close()
    st.success('Visitor database cleared successfully!')

def clearrecenthistory():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance")
    conn.commit()
    conn.close()
    shutil.rmtree(VISITOR_HISTORY, ignore_errors=True)
    os.mkdir(VISITOR_HISTORY)
    st.success('Recent history cleared successfully!')

# Initialize database
initialize_db()

# Main menu
with st.sidebar:
    selection = option_menu(
        "Main Menu",
        ["Take Attendance", "Add Person", "View Attendance", "Search Attendance", "Clear Database", "Clear Recent History"],
        icons=["camera", "person-add", "clipboard-data", "search", "trash", "clock-history"],
        menu_icon="cast",
        default_index=0
    )

if selection == "Take Attendance":
    Takeattendance()
elif selection == "Add Person":
    personadder()
elif selection == "View Attendance":
    view_attendance()
elif selection == "Search Attendance":
    search_attendance()
elif selection == "Clear Database":
    cleardatabase()
elif selection == "Clear Recent History":
    clearrecenthistory()

