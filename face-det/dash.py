import streamlit as st
from streamlit_option_menu import option_menu
from addutiles import initialize_data, add_data_db, process_image, setup_face_recognition,view_attendace,attendtaker
import pandas as pd
import numpy as np
import os
import cv2
import shutil
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
file_history    = 'visitors_history.csv' 
if st.sidebar.button('Click to Clear out all the data'):
    ## Clearing Visitor Database
    shutil.rmtree(VISITOR_DB, ignore_errors=True)
    os.mkdir(VISITOR_DB)
    ## Clearing Visitor History
    shutil.rmtree(VISITOR_HISTORY, ignore_errors=True)
    os.mkdir(VISITOR_HISTORY)

if not os.path.exists(VISITOR_DB):
    os.mkdir(VISITOR_DB)

if not os.path.exists(VISITOR_HISTORY):
    os.mkdir(VISITOR_HISTORY)
def dashboard():
    st.header("Dashboard")
    
    with st.sidebar:
        selected = option_menu("Dashboard Menu", 
                               ["Profile", 'View Attendance', 'Manage Attendance', 'Attendance History', 'ADD', 'Logout'],
                               icons=['person-circle', 'clipboard2-data', 'gear', 'clock-history', 'gear', 'box-arrow-in-right'],
                               menu_icon="cast", default_index=0)
    
    if selected == "Profile":
        attendtaker()
    elif selected == "View Attendance":
        view_attendace()
    elif selected == "Manage Attendance":
        pass
    elif selected == "Attendance History":
        pass
    elif selected == "ADD":
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        VISITOR_DB = os.path.join(ROOT_DIR, "visitor_database")
        COLOR_DARK = (0, 0, 153)
        COLOR_WHITE = (255, 255, 255)
        COLS_INFO = ['Name']
        COLS_ENCODE = [f'v{i}' for i in range(512)]
        allowed_image_type = ['.png', 'jpg', '.jpeg']
        data_path = VISITOR_DB
        file_db = os.path.join(data_path, 'visitors_db.csv')
        mtcnn, resnet, device = setup_face_recognition()
        st.markdown("## Upload or Capture a Picture")

        st.subheader("Enter Name")
        face_name = st.text_input('Name:', '', placeholder="John Doe", key='name_input')

        st.subheader("Select Image Source")
        pic_option = st.selectbox(
                'How would you like to get an image?',
                ["Upload a Picture", "Take a Picture with Cam"],
                key='pic_option'
            )
        img_file_buffer = None
        if pic_option == 'Upload a Picture':
            img_file_buffer = st.file_uploader('Upload a Picture', type=allowed_image_type, key='file_uploader')
        elif pic_option == 'Take a Picture with Cam':
            img_file_buffer = st.camera_input("Take a Picture with Cam", key='camera_input')
        if img_file_buffer is not None:
            file_bytes = np.asarray(bytearray(img_file_buffer.read()), dtype=np.uint8)
            image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            st.markdown("### Image Preview")
            st.image(image_rgb, caption='Uploaded/Captured Image', use_column_width=True, channels='RGB')

            if st.button('Save Image'):
                if len(face_name) > 1:
                    try:
                        image_path = os.path.join(VISITOR_DB, f'{face_name}.jpg')
                        with open(image_path, 'wb') as file:
                            file.write(img_file_buffer.getbuffer())
                        encodes_cur_frame = process_image(image_array, mtcnn, resnet, device)
                        if encodes_cur_frame is not None:
                            df_new = pd.DataFrame(data=encodes_cur_frame, columns=COLS_ENCODE)
                            df_new[COLS_INFO] = face_name
                            df_new = df_new[COLS_INFO + COLS_ENCODE].copy()
                            DB = initialize_data(file_db, COLS_INFO, COLS_ENCODE)
                            add_data_db(df_new, file_db)
                            st.success("Details Added Successfully!")
                        else:
                            st.error("Error processing the image.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                else:
                    st.warning("Please enter a valid name.")
        else:
            st.info("Please upload or capture an image.")
    elif selected == "Logout":
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.rerun()

if __name__ == "__main__":
    dashboard()
