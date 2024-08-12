#######################################################
import uuid ## random id generator
from streamlit_option_menu import option_menu
import streamlit as st
import os
import shutil
import cv2
import numpy as np
import pandas as pd
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageDraw
from test import test
import torch
import datetime
from utils import tts
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()
#######################################################

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VISITOR_DB = os.path.join(ROOT_DIR, "visitor_database")
VISITOR_HISTORY = os.path.join(ROOT_DIR, "visitor_history")
COLOR_DARK  = (0, 0, 153)
COLOR_WHITE = (255, 255, 255)
COLS_INFO   = ['Name']
COLS_ENCODE = [f'v{i}' for i in range(512)]
## Database
data_path       = VISITOR_DB
file_db         = 'visitors_db.csv'         ## To store user information
file_history    = 'visitors_history.csv'    ## To store visitor history information

## Image formats allowed
allowed_image_type = ['.png', 'jpg', '.jpeg']
def initialize_data():
    if os.path.exists(os.path.join(data_path, file_db)):
        # st.info('Database Found!')
        df = pd.read_csv(os.path.join(data_path, file_db))

    else:
        # st.info('Database Not Found!')
        df = pd.DataFrame(columns=COLS_INFO + COLS_ENCODE)
        df.to_csv(os.path.join(data_path, file_db), index=False)

    return df

def add_data_db(df_visitor_details):
    try:
        df_all = pd.read_csv(os.path.join(data_path, file_db))

        if not df_all.empty:
            df_all = pd.concat([df_all,df_visitor_details], ignore_index=False)
            df_all.drop_duplicates(keep='first', inplace=True)
            df_all.reset_index(inplace=True, drop=True)
            df_all.to_csv(os.path.join(data_path, file_db), index=False)
            tts('Details Added Successfully!')
            st.success('Details Added Successfully!')
        else:
            df_visitor_details.to_csv(os.path.join(data_path, file_db), index=False)
            tts('Initiated Data Successfully!')
            st.success('Initiated Data Successfully!')

    except Exception as e:
        st.error(e)

def BGR_to_RGB(image_in_array):
    return cv2.cvtColor(image_in_array, cv2.COLOR_BGR2RGB)

def attendance(id, name):
    f_p = os.path.join(VISITOR_HISTORY, file_history)
    # st.write(f_p)

    now = datetime.datetime.now()
    dtString = now.strftime('%Y-%m-%d %H:%M:%S')
    df_attendace_temp = pd.DataFrame(data={ "id"            : [id],
                                            "visitor_name"  : [name],
                                            "Timing"        : [dtString]
                                            })

    if not os.path.isfile(f_p):
        df_attendace_temp.to_csv(f_p, index=False)
        # st.write(df_attendace_temp)
    else:
        df_attendace = pd.read_csv(f_p)
        df_attendace = pd.concat([df_attendace,df_attendace_temp])
        df_attendace.to_csv(f_p, index=False)
############################################################################
# for Viewing attendace
def view_attendace():
    f_p = os.path.join(VISITOR_HISTORY, file_history)
    df_attendance_temp = pd.DataFrame(columns=["id", "visitor_name", "Timing"])

    if not os.path.isfile(f_p):
        df_attendance_temp.to_csv(f_p, index=False)
    else:
        df_attendance_temp = pd.read_csv(f_p)

    df_attendance = df_attendance_temp.sort_values(by='Timing', ascending=False)
    df_attendance.reset_index(inplace=True, drop=True)

    # Add a column for image file paths
    image_paths = []
    for idx, row in df_attendance.iterrows():
        image_path = None
        files = [file for file in os.listdir(VISITOR_HISTORY)
                 if file.endswith(tuple(allowed_image_type)) and file.startswith(str(row['id']))]
        if files:
            image_path = os.path.join(VISITOR_HISTORY, files[0])
        image_paths.append(image_path)
    
    df_attendance['image_path'] = image_paths

    # Display DataFrame and images
    import base64
    def encode_image(image_path):
        if os.path.isfile(image_path):
            with open(image_path, "rb") as image_file:
                return "data:image/jpeg;base64," + base64.b64encode(image_file.read()).decode()
        return None
    df_attendance['image'] = df_attendance['image_path'].apply(encode_image)

    # Display DataFrame with images using st.data_editor
    st.data_editor(
        df_attendance.drop(columns=["image_path"]),
        column_config={
            "id": st.column_config.Column("ID"),
            "visitor_name": st.column_config.Column("Visitor Name"),
            "Timing": st.column_config.Column("Timing"),
            "image": st.column_config.ImageColumn(
                "Visitor Image", help="Preview of visitor images"
            )
        },
        hide_index=True,
        use_container_width=True
    )

##########################################################################
def crop_image_with_ratio(img, height,width,middle):
    h, w = img.shape[:2]
    h=h-h%4
    new_w = int(h / height)*width
    startx = middle - new_w //2
    endx=middle+new_w //2
    if startx<=0:
        cropped_img = img[0:h, 0:new_w]
    elif endx>=w:
        cropped_img = img[0:h, w-new_w:w]
    else:
        cropped_img = img[0:h, startx:endx]
    return cropped_img

################################################### Defining Static Data ###############################################



###################### Defining Static Paths ###################4
def cleardatabase():
    shutil.rmtree(VISITOR_DB, ignore_errors=True)
    os.mkdir(VISITOR_DB)
    # ## Clearing Visitor History
    # shutil.rmtree(VISITOR_HISTORY, ignore_errors=True)
    # os.mkdir(VISITOR_HISTORY)
    
    if not os.path.exists(VISITOR_DB):
        os.mkdir(VISITOR_DB)
    
    # if not os.path.exists(VISITOR_HISTORY):
    #     os.mkdir(VISITOR_HISTORY)
def clearrecenthistory():
    shutil.rmtree(VISITOR_HISTORY, ignore_errors=True)
    os.mkdir(VISITOR_HISTORY)
    if not os.path.exists(VISITOR_HISTORY):
        os.mkdir(VISITOR_HISTORY)
# st.write(VISITOR_HISTORY)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
mtcnn = MTCNN(
        image_size=160, margin=0, min_face_size=20,
        thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
        device=device,keep_all=True
        )
########################################################################################################################

###############################################################
#this is for taking attendance
def Takeattendance():
    visitor_id = uuid.uuid1()
    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        image_array = cv2.imdecode(np.frombuffer(bytes_data,np.uint8),cv2.IMREAD_COLOR)
        image_array_copy = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        with open(os.path.join(VISITOR_HISTORY,f'{visitor_id}.jpg'), 'wb') as file:
            file.write(img_file_buffer.getbuffer())
            tts('Image Saved Successfully!')
            st.success('Image Saved Successfully!')
            max_faces = 0
            rois = []  
            aligned=[]
            spoofs=[]
            can=[]
            face_locations ,prob = mtcnn(image_array,return_prob=True)
            boxes, _ = mtcnn.detect(image_array)
            boxes_int=boxes.astype(int)
            if face_locations is not None:
                for idx, (left,top, right, bottom) in enumerate(boxes_int):
                    img=crop_image_with_ratio(image_array,4,3,(left+right)//2)
                    spoof=test(img,"./resources/anti_spoof_models",device)
                    if spoof<=1:
                        spoofs.append("REAL")
                        can.append(idx)
                    else:
                        spoofs.append("FAKE")
                #this is to show if the image is real or not
            for idx,  (left,top, right, bottom) in enumerate(boxes_int):
                rois.append(image_array[top:bottom, left:right].copy())
                cv2.rectangle(image_array, (left, top), (right, bottom), COLOR_DARK, 2)
                cv2.rectangle(image_array, (left, bottom + 35), (right, bottom), COLOR_DARK, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image_array, f"#{idx} {spoofs[idx]}", (left + 5, bottom + 25), font, .55, COLOR_WHITE, 1)
            #this is for hiding image of if its fake or real
            # st.image(BGR_to_RGB(image_array), width=720)
            # this is to detect whether he is real or fake
            # st.write(spoofs[idx])
            if spoofs[idx] == "REAL":
                tts("Its an Real Image")
                st.success("Its an Real Image")
            elif spoofs[idx] == "FAKE":
                tts("Its an Fake Image")
                st.error("Its an Fake Image")
            max_faces = len(boxes_int)
            if max_faces > 0:
                col1, col2 = st.columns(2)
                face_idxs = col1.multiselect("Select face#", can,
                                             default=can)
                similarity_threshold = col2.slider('Select Threshold for Similarity',
                                                     min_value=0.0, max_value=3.0,
                                                     value=0.5)
                flag_show = False
                if st.button("Mark Attendance")& (len(face_idxs)>0):
                    dataframe_new = pd.DataFrame()
                    for idx,loc in enumerate(face_locations) :
                        torch_loc = torch.stack([loc]).to(device)
                        encodesCurFrame = resnet(torch_loc).detach().cpu()
                        aligned.append(encodesCurFrame)
                    for face_idx in face_idxs:
                        database_data = initialize_data()
                        face_encodings  = database_data[COLS_ENCODE].values
                        dataframe = database_data[COLS_INFO]
                        if len(aligned) < 1:
                            tts(f'Please Try Again for face#{face_idx}!')
                            st.error(f'Please Try Again for face#{face_idx}!')
                        else:
                            face_to_compare = aligned[face_idx].numpy()
                            dataframe['similarity'] = [np.linalg.norm(e1 - face_to_compare) for e1 in face_encodings]
                            dataframe['similarity'] = dataframe['similarity'].astype(float)
                            dataframe_new = dataframe.drop_duplicates(keep='first')
                            dataframe_new.reset_index(drop=True, inplace=True)
                            dataframe_new.sort_values(by="similarity", ascending=True, inplace=True)
                            dataframe_new = dataframe_new[dataframe_new['similarity'] < similarity_threshold].head(1)
                            dataframe_new.reset_index(drop=True, inplace=True)
                            if dataframe_new.shape[0]>0:
                                (left,top, right, bottom) = (boxes_int[face_idx])
                                rois.append(image_array_copy[top:bottom, left:right].copy())
                                cv2.rectangle(image_array_copy, (left, top), (right, bottom), COLOR_DARK, 2)
                                cv2.rectangle(image_array_copy, (left, bottom + 35), (right, bottom), COLOR_DARK, cv2.FILLED)
                                font = cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(image_array_copy, f"#{dataframe_new.loc[0, 'Name']}", (left + 5, bottom + 25), font, .55, COLOR_WHITE, 1)
                                name_visitor = dataframe_new.loc[0, 'Name']
                                attendance(visitor_id, name_visitor)
                                flag_show = True
                            else:
                                tts(f'No Match Found for the given Similarity Threshold! for face#{face_idx}')
                                st.error(f'No Match Found for the given Similarity Threshold! for face#{face_idx}')
                                st.info('Please Update the database for a new person or click again!')
                                tts('Please Update the database for a new person or click again!')
                                attendance(visitor_id, 'Unknown')
                    if flag_show == True:
                        st.image(BGR_to_RGB(image_array_copy), width=720)
                        tts("Attendance Marked succesfully")
                        st.success("Attendance Marked succesfully")
            else:
                tts('No human face detected.')
                st.error('No human face detected.')
####################################################################################
# For adding person
def send_email(recipient_email, subject, body):
    sender_email = os.getenv('SMTP_USERNAME')
    sender_password = os.getenv('SMTP_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server and port
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        st.success(f"Unique ID sent to {recipient_email}")
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")

def personadder():
    face_name = st.text_input('Name:', '')
    email = st.text_input('Email:', '')

    # Initialize img_file_buffer
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

    if ((img_file_buffer is not None) & (len(face_name) > 1) & st.button('Image Preview', use_container_width=True)):
        tts("Previewing image")
        st.subheader("Image Preview")
        st.image(img_file_buffer)

    if ((img_file_buffer is not None) & (len(face_name) > 1) & (len(email) > 1) & st.button('Click to Save!', use_container_width=True)):
        unique_id = str(uuid.uuid4())
        image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image_array is None:
            st.error("Error loading the image. Please try again.")
            return

        with open(os.path.join(VISITOR_DB, f'{face_name}_{unique_id}.jpg'), 'wb') as file:
            file.write(img_file_buffer.getbuffer())

        # Convert image to RGB before face detection
        image_array_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        face_locations, prob = mtcnn(image_array_rgb, return_prob=True)

        if face_locations is None or len(face_locations) == 0:
            st.error("No faces detected in the image. Please try again.")
            st.write("Debugging Info:")
            st.write(f"Image shape: {image_array.shape}")
            st.write(f"Face locations: {face_locations}")
            return

        torch_loc = torch.stack([face_locations[0]]).to(device)
        encodesCurFrame = resnet(torch_loc).detach().cpu()

        df_new = pd.DataFrame(data=encodesCurFrame, columns=COLS_ENCODE)
        df_new[COLS_INFO] = face_name
        df_new['Unique_ID'] = unique_id  # Add the unique ID to the DataFrame
        df_new = df_new[['Unique_ID'] + COLS_INFO + COLS_ENCODE].copy()

        DB = initialize_data()
        add_data_db(df_new)

        # Send email with unique ID
        email_body = f"Hello {face_name},\n\nYour unique ID is: {unique_id}\n\nBest regards,\nTeam"
        send_email(email, "Your Unique ID", email_body)

