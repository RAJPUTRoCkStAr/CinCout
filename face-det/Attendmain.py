import uuid
from streamlit_option_menu import option_menu
import streamlit as st
import os
import shutil
import cv2
import numpy as np
import pandas as pd
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageDraw
import torch
import datetime
import base64
from utils import tts
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import sqlite3
import random,string
from test import test

load_dotenv()
allowed_image_type = ['.png', 'jpg', '.jpeg']
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VISITOR_DB = os.path.join(ROOT_DIR, "visitor_database")
VISITOR_HISTORY = os.path.join(ROOT_DIR, "visitor_history")
COLOR_DARK  = (0, 0, 153)
COLOR_WHITE = (255, 255, 255)
COLS_INFO   = ['Name']
COLS_ENCODE = [f'v{i}' for i in range(512)]
DB_PATH     = os.path.join(ROOT_DIR, "data/database.db")
def generate_10_digit_id():
    uuid_int = uuid.uuid4().int
    alphanumeric_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    numeric_part = str(uuid_int % 1000000).zfill(4)
    return alphanumeric_id + numeric_part
def BGR_to_RGB(image_in_array):
    return cv2.cvtColor(image_in_array, cv2.COLOR_BGR2RGB)
## Database
def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables if they do not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitors (
        Unique_ID TEXT PRIMARY KEY,
        Name TEXT NOT NULL,
        {columns}
    )
    '''.format(columns=', '.join(f'{col} REAL' for col in COLS_ENCODE)))

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

def add_data_db(visitor_details):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for _, row in visitor_details.iterrows():
        cursor.execute('''
        INSERT OR REPLACE INTO visitors (Unique_ID, Name, {columns})
        VALUES (?, ?, {placeholders})
        '''.format(columns=', '.join(COLS_ENCODE),
                   placeholders=', '.join('?' * len(COLS_ENCODE))),
                   (row['Unique_ID'], row['Name'], *row[COLS_ENCODE]))
    
    conn.commit()
    conn.close()
    tts('Details Added Successfully!')
    st.success('Details Added Successfully!')

def get_data_from_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM visitors
    ''')
    data = cursor.fetchall()
    conn.close()
    
    df = pd.DataFrame(data, columns=['Unique_ID', 'Name'] + COLS_ENCODE)
    return df

def add_attendance(id, name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.datetime.now()
    dtString = now.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO attendance (ID, visitor_name, Timing, Image_Path)
    VALUES (?, ?, ?, ?)
    ''', (id, name, dtString, f'{id}.jpg'))
    
    conn.commit()
    conn.close()

def get_attendance_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM attendance
    ''')
    data = cursor.fetchall()
    conn.close()
    
    df = pd.DataFrame(data, columns=['ID', 'visitor_name', 'Timing', 'Image_Path'])
    return df

def crop_image_with_ratio(img, height, width, middle):
    h, w = img.shape[:2]
    h = h - h % 4
    new_w = int(h / height) * width
    startx = middle - new_w // 2
    endx = middle + new_w // 2
    if startx <= 0:
        cropped_img = img[0:h, 0:new_w]
    elif endx >= w:
        cropped_img = img[0:h, w-new_w:w]
    else:
        cropped_img = img[0:h, startx:endx]
    return cropped_img
def connect_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    return conn
def cleardatabase():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM visitors")
    
    conn.commit()
    conn.close()
    
    tts('Visitor database cleared successfully!')
    st.success('Visitor database cleared successfully!')

    if not os.path.exists(VISITOR_DB):
        os.mkdir(VISITOR_DB)
    
def clearrecenthistory():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Clear all entries from the attendance table
    cursor.execute("DELETE FROM attendance")
    
    conn.commit()
    conn.close()
    
    # Optionally, remove the image history
    shutil.rmtree(VISITOR_HISTORY, ignore_errors=True)
    os.mkdir(VISITOR_HISTORY)
    
    tts('Recent history cleared successfully!')
    st.success('Recent history cleared successfully!')

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
mtcnn = MTCNN(
        image_size=160, margin=0, min_face_size=20,
        thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
        device=device, keep_all=True
        )
def view_registered_persons():
    st.write("### Registered Persons")
    df_registered = get_data_from_db()
    if df_registered.empty:
        st.warning("No registered persons found.")
        return
    df_registered = df_registered[['Unique_ID', 'Name','email','category']] 
    st.dataframe(df_registered, use_container_width=True,hide_index=True)
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
                "image": st.column_config.ImageColumn(
                    "Visitor Image", help="Preview of visitor images"
                )
            },
            hide_index=True,
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error displaying attendance data: {e}")

def Takeattendance():
    visitor_id = st.text_input("Enter your Unique ID:", '')

    if st.button("Mark Attendance"):
        if not visitor_id:
            st.error("Please enter your Unique ID.")
            return
    
        img_file_buffer = st.camera_input("Take a picture")
        
        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            image_array = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            image_array_copy = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            with open(os.path.join(VISITOR_HISTORY, f'{visitor_id}.jpg'), 'wb') as file:
                file.write(img_file_buffer.getbuffer())
                tts('Image Saved Successfully!')
                st.success('Image Saved Successfully!')
                
                boxes, probs = mtcnn.detect(image_array, landmarks=False)
                if boxes is not None:
                    boxes_int = [[int(box[0]), int(box[1]), int(box[2]), int(box[3])] for box in boxes]
                    aligned = []
                    rois = []
                    spoofs = []
                    can = []
                    fake_detected = False
                    attendance_marked = False
                    
                    for idx, box in enumerate(boxes):
                        left, top, right, bottom = map(int, box)
                        face = crop_image_with_ratio(image_array, 160, 160, int((left + right) / 2))
                        aligned_face = mtcnn(face)
                        
                        if aligned_face is not None:
                            encodesCurFrame = resnet(aligned_face.to(device)).detach().cpu()
                            aligned.append(encodesCurFrame)
                            
                            # Anti-spoofing check
                            spoof_score = test(face, "./resources/anti_spoof_models", device)
                            if spoof_score <= 1:
                                spoofs.append("REAL")
                                can.append(idx)
                            else:
                                spoofs.append("FAKE")
                                fake_detected = True
                        else:
                            spoofs.append("UNKNOWN")
                    
                    for idx, (left, top, right, bottom) in enumerate(boxes_int):
                        if idx < len(spoofs):
                            cv2.rectangle(image_array, (left, top), (right, bottom), COLOR_DARK, 2)
                            cv2.rectangle(image_array, (left, bottom + 35), (right, bottom), COLOR_DARK, cv2.FILLED)
                            font = cv2.FONT_HERSHEY_DUPLEX
                            cv2.putText(image_array, f"#{idx} {spoofs[idx]}", (left + 5, bottom + 25), font, .55, COLOR_WHITE, 1)
                        
                            # Show real or fake status
                            if spoofs[idx] == "REAL":
                                st.success("The detected face is REAL.")
                                tts("The detected face is REAL.")
                            elif spoofs[idx] == "FAKE":
                                st.error("The detected face is FAKE.")
                                tts("The detected face is FAKE.")
                        
                    if len(aligned) > 0 and not fake_detected:
                        similarity_threshold = 0.5
                        flag_show = False
                        
                        for face_idx in can:
                            database_data = get_data_from_db()
                            face_encodings = database_data[COLS_ENCODE].values
                            dataframe = database_data[COLS_INFO]
                            
                            face_to_compare = aligned[face_idx].numpy()
                            similarity = np.dot(face_encodings, face_to_compare.T)
                            matches = similarity > similarity_threshold
                            
                            if matches.any():
                                idx = np.argmax(similarity[matches])
                                dataframe_new = dataframe.iloc[idx]
                                name_visitor = dataframe_new['Name']
                                add_attendance(visitor_id, name_visitor)
                                flag_show = True
                                
                                (left, top, right, bottom) = boxes_int[face_idx]
                                rois.append(image_array_copy[top:bottom, left:right].copy())
                                cv2.rectangle(image_array_copy, (left, top), (right, bottom), COLOR_DARK, 2)
                                cv2.rectangle(image_array_copy, (left, bottom + 35), (right, bottom), COLOR_DARK, cv2.FILLED)
                                font = cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(image_array_copy, f"#{name_visitor}", (left + 5, bottom + 25), font, .55, COLOR_WHITE, 1)
                            else:
                                st.error('No Match Found for the given Similarity Threshold!')
                                tts('No Match Found for the given Similarity Threshold!')
                                st.info('Please Update the database for a new person or click again!')
                                tts('Please Update the database for a new person or click again!')
                                add_attendance(visitor_id, 'Unknown')
                        
                        if flag_show:
                            st.image(BGR_to_RGB(image_array_copy), width=720)
                            tts("Attendance Marked successfully")
                            st.success("Attendance Marked successfully")
                        else:
                            tts("Attendance not marked due to no match found.")
                            st.warning("Attendance not marked due to no match found.")
                    elif fake_detected:
                        st.error("Attendance not marked because the image is FAKE.")
                        tts("Attendance not marked because the image is FAKE.")
                    else:
                        st.error('No Real Face Detected.')
                        tts('No Real Face Detected.')
                else:
                    st.error('No human face detected.')
                    tts('No human face detected.')
    
def send_email(recipient_email, subject, body):
    sender_email = os.getenv('SMTP_USERNAME')
    sender_password = os.getenv('SMTP_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    html_body = f"""
    <html>
    <body>
        <h2 style="color: #4CAF50;">Hello {recipient_email.split('@')[0]},</h2>
        <p style="font-size: 14px; color: #333;">{body}</p>
        <br>
        <p style="font-size: 12px; color: #999;">Best regards,<br>Team</p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        st.success(f"Unique ID sent to {recipient_email}")
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")

def ensure_category_email_columns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure Category and Email columns exist
    cursor.execute("PRAGMA table_info(visitors)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'Category' not in columns:
        cursor.execute("ALTER TABLE visitors ADD COLUMN Category TEXT")

    if 'Email' not in columns:
        cursor.execute("ALTER TABLE visitors ADD COLUMN Email TEXT")
    if 'image_path' not in columns:
        cursor.execute("ALTER TABLE visitors ADD COLUMN image_path TEXT")

    conn.commit()
    conn.close()

def personadder():
    face_name = st.text_input('Name:', '')
    email = st.text_input('Email:', '')

    category = st.selectbox('Select Category', ['School', 'Office', 'University', 'Hospital'])

    img_file_buffer = None
    pic_option = st.selectbox('Upload Picture',
                              options=["Upload your Profile Picture", "Take a Picture with Cam"], index=None)

    if pic_option == 'Upload your Profile Picture':
        img_file_buffer = st.file_uploader('Upload a Picture', type=allowed_image_type)
        if img_file_buffer is not None:
            file_bytes = np.asarray(bytearray(img_file_buffer.read()), dtype=np.uint8)

    elif pic_option == 'Take a Picture with Cam':
        img_file_buffer = st.camera_input("Take a Picture with Cam")
        if img_file_buffer is not None:
            file_bytes = np.frombuffer(img_file_buffer.getvalue(), np.uint8)

    if img_file_buffer is not None and len(face_name) > 1 and st.button('Image Preview', use_container_width=True):
        tts("Previewing image")
        st.subheader("Image Preview")
        st.image(img_file_buffer)

    if img_file_buffer is not None and len(face_name) > 1 and len(email) > 1 and st.button('Click to Save!', use_container_width=True):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Ensure the Category and Email columns exist
        ensure_category_email_columns()

        # Check if the person or email already exists in the selected category
        cursor.execute("SELECT * FROM visitors WHERE (Name = ? OR Email = ?) AND Category = ?", (face_name, email, category))
        existing_person = cursor.fetchone()

        if existing_person:
            st.warning(f"A person with the name '{face_name}' or email '{email}' already exists in {category}.")
            tts(f"A person with the name '{face_name}' or email '{email}' already exists in {category}.")
            conn.close()
            return

        # Generate unique ID
        unique_id = generate_10_digit_id()

        # Decode and save the image
        image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image_array is None:
            st.error("Error loading the image. Please try again.")
            conn.close()
            return

        # Save image to disk
        image_path = os.path.join(VISITOR_DB, f'{face_name}_{unique_id}.jpg')
        with open(image_path, 'wb') as file:
            file.write(img_file_buffer.getbuffer())

        # Encode the face
        image_array_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        face_locations, prob = mtcnn(image_array_rgb, return_prob=True)

        if face_locations is None or len(face_locations) == 0:
            st.error("No faces detected in the image. Please try again.")
            conn.close()
            return

        torch_loc = torch.stack([face_locations[0]]).to(device)
        encodesCurFrame = resnet(torch_loc).detach().cpu()

        # Add data to the database
        cursor.execute("""
            INSERT INTO visitors (Unique_ID, Name, Category, Email, Image_Path) 
            VALUES (?, ?, ?, ?, ?)
        """, (unique_id, face_name, category, email, image_path))

        conn.commit()
        conn.close()

        # Send confirmation email
        email_body = f"Hello {face_name},\n\nYour unique ID is: {unique_id}\n\nBest regards,\nTeam"
        send_email(email, "Your Unique ID", email_body)
        
        st.success(f"{face_name} has been added successfully!")
        tts(f"{face_name} has been added successfully!")
def search_attendance():
    st.header("Search Attendance Records")
    
    search_type = st.selectbox("Search by", ["Visitor ID", "Name"])
    search_input = st.text_input(f"Enter {search_type} to search:", '')

    searchatt = st.button('Search Attendance',use_container_width=True,type='primary')
    clearatt = st.button('Clear Recent Attendance',use_container_width=True,type='secondary')
    if clearatt:
        clearrecenthistory()
    if searchatt:
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
                        "image": st.column_config.ImageColumn(
                            "Visitor Image", help="Preview of visitor images"
                        )
                    },
                    hide_index=True,
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error displaying search results: {e}")
        else:
            st.warning(f"No records found for {search_type}: {search_input}")

initialize_db()
