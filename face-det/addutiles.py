import pandas as pd
import os
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import cv2
import streamlit as st
import datetime
import uuid
from test import test
from PIL import Image, ImageDraw
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
mtcnn = MTCNN(
        image_size=160, margin=0, min_face_size=20,
        thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
        device=device,keep_all=True
        )
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
            st.success('Details Added Successfully!')
        else:
            df_visitor_details.to_csv(os.path.join(data_path, file_db), index=False)
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
def initialize_data(file_db, cols_info, cols_encode):
    if os.path.exists(file_db):
        df = pd.read_csv(file_db)
    else:
        df = pd.DataFrame(columns=cols_info + cols_encode)
        df.to_csv(file_db, index=False)
    return df

def add_data_db(df_visitor_details, file_db):
    try:
        if os.path.exists(file_db):
            df_all = pd.read_csv(file_db)
            df_all = pd.concat([df_all, df_visitor_details], ignore_index=True)
            df_all.drop_duplicates(keep='first', inplace=True)
            df_all.reset_index(inplace=True, drop=True)
            df_all.to_csv(file_db, index=False)
            st.success('Details Added Successfully!')
        else:
            df_visitor_details.to_csv(file_db, index=False)
            st.success('Initiated Data Successfully!')
    except Exception as e:
        st.error(f"Error: {e}")

def process_image(image_array, mtcnn, resnet, device):
    # Convert to RGB if the image is in BGR format
    if image_array.shape[2] == 3 and image_array.shape[0] != 3:
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

    # Perform face detection
    face_locations, prob = mtcnn(image_array, return_prob=True)


    if face_locations is not None and len(face_locations) > 0:
        st.image(image_array, caption='Detected Image', channels='RGB')  # Display the image
        torch_loc = torch.stack([face_locations[0]]).to(device)
        encodes_cur_frame = resnet(torch_loc).detach().cpu()
        return encodes_cur_frame
    else:
        st.error("No face detected.")
        # Optional: Display the image even if no face is detected
        st.image(image_array, caption='Image with No Face Detected', channels='RGB')
        return None


def setup_face_recognition():
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20,
                  thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
                  device=device, keep_all=True)
    return mtcnn, resnet, device

#####################################################################################################
# View attendance
allowed_image_type = ['.png', 'jpg', '.jpeg']
file_history    = 'visitors_history.csv' 
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VISITOR_HISTORY = os.path.join(ROOT_DIR, "visitor_history")
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
def view_attendace():
    f_p = os.path.join(VISITOR_HISTORY, file_history)
    # st.write(f_p)
    df_attendace_temp = pd.DataFrame(columns=["id",
                                              "visitor_name", "Timing"])

    if not os.path.isfile(f_p):
        df_attendace_temp.to_csv(f_p, index=False)
    else:
        df_attendace_temp = pd.read_csv(f_p)

    df_attendace = df_attendace_temp.sort_values(by='Timing',
                                                 ascending=False)
    df_attendace.reset_index(inplace=True, drop=True)

    st.write(df_attendace)

    if df_attendace.shape[0]>0:
        id_chk  = df_attendace.loc[0, 'id']
        id_name = df_attendace.loc[0, 'visitor_name']

        selected_img = st.selectbox('Search Image using ID',
                                    options=['None']+list(df_attendace['id']))

        avail_files = [file for file in list(os.listdir(VISITOR_HISTORY))
                       if ((file.endswith(tuple(allowed_image_type))) &
                        (file.startswith(selected_img) == True))]

        if len(avail_files)>0:
            selected_img_path = os.path.join(VISITOR_HISTORY,
                                             avail_files[0])
            #st.write(selected_img_path)

            ## Displaying Image
            st.image(Image.open(selected_img_path))

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

#########################################################################################################################################################
#attendance detection
def attendtaker():
    visitor_id = uuid.uuid1()
    img_file_buffer = st.camera_input("Take a picture")
    
    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        image_array = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        image_array_copy = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        # Saving Visitor History
        with open(os.path.join(VISITOR_HISTORY, f'{visitor_id}.jpg'), 'wb') as file:
            file.write(img_file_buffer.getbuffer())
            st.success('Image Saved Successfully!')

        # Validating Image
        max_faces = 0
        rois = []  # Region of interests (arrays of face areas)
        aligned = []
        spoofs = []
        can = []

        # Get location of Face from Image
        face_locations, prob = mtcnn(image_array, return_prob=True)
        boxes, _ = mtcnn.detect(image_array)
        boxes_int = boxes.astype(int)

        if face_locations is not None:
            for idx, (left, top, right, bottom) in enumerate(boxes_int):
                img = crop_image_with_ratio(image_array, 4, 3, (left + right) // 2)
                spoof = test(img, "./resources/anti_spoof_models", device)
                if spoof <= 1:
                    spoofs.append("REAL")
                    can.append(idx)
                else:
                    spoofs.append("FAKE")

            for idx, (left, top, right, bottom) in enumerate(boxes_int):
                rois.append(image_array[top:bottom, left:right].copy())
                cv2.rectangle(image_array, (left, top), (right, bottom), COLOR_DARK, 2)
                cv2.rectangle(image_array, (left, bottom + 35), (right, bottom), COLOR_DARK, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image_array, f"#{idx} {spoofs[idx]}", (left + 5, bottom + 25), font, .55, COLOR_WHITE, 1)

            st.image(BGR_to_RGB(image_array), width=720)
            max_faces = len(boxes_int)

            if max_faces > 0:
                col1, col2 = st.columns(2)
                face_idxs = col1.multiselect("Select face#", can, default=can)
                similarity_threshold = col2.slider('Select Threshold for Similarity', min_value=0.0, max_value=3.0, value=0.5)
                flag_show = False

                if col1.checkbox('Click to proceed!') and len(face_idxs) > 0:
                    dataframe_new = pd.DataFrame()
                    for idx, loc in enumerate(face_locations):
                        torch_loc = torch.stack([loc]).to(device)
                        encodesCurFrame = resnet(torch_loc).detach().cpu()
                        aligned.append(encodesCurFrame)

                    # Initialize database
                    database_data = initialize_data(file_db, COLS_INFO, COLS_ENCODE)

                    face_encodings = database_data[COLS_ENCODE].values
                    dataframe = database_data[COLS_INFO]

                    if len(aligned) < 1:
                        st.error(f'Please Try Again for face#{face_idx}!')
                    else:
                        for face_idx in face_idxs:
                            face_to_compare = aligned[face_idx].numpy()
                            dataframe['similarity'] = [np.linalg.norm(e1 - face_to_compare) for e1 in face_encodings]
                            dataframe['similarity'] = dataframe['similarity'].astype(float)
                            dataframe_new = dataframe.drop_duplicates(keep='first')
                            dataframe_new.reset_index(drop=True, inplace=True)
                            dataframe_new.sort_values(by="similarity", ascending=True, inplace=True)
                            dataframe_new = dataframe_new[dataframe_new['similarity'] < similarity_threshold].head(1)
                            dataframe_new.reset_index(drop=True, inplace=True)

                            if dataframe_new.shape[0] > 0:
                                (left, top, right, bottom) = (boxes_int[face_idx])
                                rois.append(image_array_copy[top:bottom, left:right].copy())
                                cv2.rectangle(image_array_copy, (left, top), (right, bottom), COLOR_DARK, 2)
                                cv2.rectangle(image_array_copy, (left, bottom + 35), (right, bottom), COLOR_DARK, cv2.FILLED)
                                font = cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(image_array_copy, f"#{dataframe_new.loc[0, 'Name']}", (left + 5, bottom + 25), font, .55, COLOR_WHITE, 1)
                                name_visitor = dataframe_new.loc[0, 'Name']
                                attendance(visitor_id, name_visitor)
                                flag_show = True
                            else:
                                st.error(f'No Match Found for the given Similarity Threshold! for face#{face_idx}')
                                st.info('Please Update the database for a new person or click again!')
                                attendance(visitor_id, 'Unknown')

                    if flag_show:
                        st.image(BGR_to_RGB(image_array_copy), width=720)
            else:
                st.error('No human face detected.')