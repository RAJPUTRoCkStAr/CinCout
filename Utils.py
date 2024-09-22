#####################################################################
#Importing of all required modules
from email.mime.multipart import MIMEMultipart
from streamlit_option_menu import option_menu
from email.mime.text import MIMEText
import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import random
import string
import smtplib
import sqlite3
import base64
import re
import os
from streamlit_TTS import auto_play,text_to_speech,text_to_audio
################################################################
#text-to-speech

def tts(text):
    # text_to_speech(text=text, language='en')
    audio=text_to_audio(text=text,language='en')
    #then play it
    # auto_play(audio)
    # audio=text_to_audio("Choose a language, type some text, and click 'Speak it out!'.",language='en')
#then play it
    auto_play(audio)

    lang='en'
    text=text

    if lang and text:
    #plays the audio directly
        text_to_speech(text=text, language=lang)
    

####################################################################

####################################################################
#generate username
def generate_username(name):
    base_name = name.lower().replace(' ', '')
    random_suffix = ''.join(random.choices(string.digits, k=4))
    username = f"{base_name}{random_suffix}"
    return username
####################################################################
#extract name from username
def extract_name(username):
    return ''.join(filter(str.isalpha, username))
######################################################################
#job roles
job_roles = {
    "School": ["Teacher", "Principal", "Counselor", "Custodian", 
               "Vice Principal", "Librarian", "Special Education Teacher", 
               "Substitute Teacher", "School Nurse", "Coach", 
               "Administrative Assistant"],
    "University": ["Professor", "Registrar", "Academic Advisor", "Researcher", 
                   "Associate Professor", "Lecturer", "Teaching Assistant", 
                   "Department Coordinator", "Admissions Officer", "Career Counselor", 
                   "Financial Aid Advisor", "Lab Technician", "IT Support"],
    "Hospital": ["Physician", "Nurse", "Technician", "Administrator", 
                 "Surgeon", "Anesthesiologist", "Medical Assistant", 
                 "Radiologic Technologist", "Physical Therapist", 
                 "Occupational Therapist", "Pharmacist", "Laboratory Technician", 
                 "Billing and Coding Specialist", "Patient Care Technician", 
                 "Phlebotomist", "Dietary Aide", "Housekeeping Staff"],
    "Office": ["Manager", "Assistant", "IT Specialist", "HR Specialist", 
               "Receptionist", "Office Manager", "Executive Assistant", 
               "Operations Manager", "Project Manager", "Marketing Manager", 
               "Accountant", "Financial Analyst", "Sales Representative", 
               "Customer Service Representative", "Network Administrator"]
}
######################################################################
# for title and pages setting
def title():
    st.set_page_config(page_title="C-in C-out",layout="wide",page_icon='media/logo.png')
    title_webapp    = "C-in C-out"
    logo_path = "media/logo.png"
    with open(logo_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    html_temp =f"""
        <div style="background-color:transparent;padding:12px;display:flex;align-items:center;">
            <img src="data:image/png;base64,{encoded_string}" style="width:100px;height:auto;margin-right:20px;">
            <div style="flex-grow:1;text-align:center;">
                <h1 style="color:white;font-size: 60px;">{title_webapp}</h1>
            </div>
        </div>  
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    background_image = """
    <style>

    [data-testid="stAppViewContainer"] {
        background-image: url("https://raw.githubusercontent.com/RAJPUTRoCkStAr/Human-activity/main/media/background.gif") !important;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed; /* Keep the background fixed during scrolling */
        height: 100vh; /* Full viewport height */
        width: 100vw; /* Full viewport width */
        overflow: hidden; /* Prevent scrolling for the container */
    }
    [data-testid="stSidebar"] {
        background-color: transparent;  /* Adds transparency to the sidebar */
        height: 100vh; /* Ensure sidebar height is the same as the viewport */
    }
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0); /* Transparent header */
    }
    [data-testid="stToolbar"] {
        right: 2rem;
    }
    button[kind="sidebar"] {
        background-color:transparent;  /* Ensures sidebar button is transparent */
    }
    </style>
    """
    st.markdown(background_image, unsafe_allow_html=True)
#     st.markdown("""
#     <style>
#         .reportview-container {
#             margin-top: -2em;
#         }
#         #MainMenu {visibility: hidden;}
#         .stDeployButton {display:none;}
#         footer {visibility: hidden;}
#         #stDecoration {display:none;}
#         header {visibility: hidden;}
#     </style>
# """, unsafe_allow_html=True)
    
#################################################################################
#database connection
conn = sqlite3.connect('Data/database.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
     name TEXT, 
     job_role TEXT, 
     email TEXT, 
     username TEXT UNIQUE, 
     password TEXT,
     item TEXT,
     place_name TEXT)
''')
conn.commit()
##############################################################################
#sign up
def signup(item):
    conn = sqlite3.connect('Data/database.db') 
    c = conn.cursor()
    st.markdown(f"<h2 style='text-align: center;color:white'>Sign Up for {item} Management</h2>", unsafe_allow_html=True)
    with st.form(key="signup_form", clear_on_submit=True):
        name = st.text_input("Enter your name")
        job_role = st.selectbox("Select your job role", job_roles[item])
        place_name = st.text_input(f"Enter your {item.lower()} name")
        email = st.text_input("Enter your email address")
        password = st.text_input("Enter your password", type="password")
        st.caption("Your password must be at least 7 characters in length and include a combination of uppercase and lowercase letters, numbers, and special characters.")
        submitted = st.form_submit_button("Sign Up")
        
        if submitted:
            if not name or not email or not password or not place_name:
                st.error("Please fill in all required fields.")
                tts("Please fill in all required fields.")
            elif not re.match(r"^[A-Za-z\s]+$", name):
                st.error("Name should contain only alphabets and spaces.")
                tts("Name should contain only alphabets and spaces.")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address.")
                tts("Please enter a valid email address.")
            elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{7,}$', password):
                st.error("Password must be at least 7 characters long and contain a mixture of symbols, capital letters, small letters, and numbers.")
                tts("Password must be at least 7 characters long and contain a mixture of symbols, capital letters, small letters, and numbers.")
            else:
                c.execute('''
                    SELECT * FROM users 
                    WHERE name = ? AND email = ? AND job_role = ? AND place_name = ? AND item = ?
                ''', (name, email, job_role, place_name, item))
                if c.fetchone():
                    st.error('A user with the same name, email, job role, and place name already exists. Please try again.')
                    tts('A user with the same name, email, job role, and place name already exists. Please try again.')
                else:
                    username = generate_username(name)
                    c.execute('SELECT * FROM users WHERE username = ?', (username,))
                    if c.fetchone() is None:
                        c.execute('INSERT INTO users (name, job_role, email, username, password, item, place_name) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                                  (name, job_role, email, username, password, item, place_name))
                        conn.commit()
                        with st.spinner("Processing your registration... Please wait while we send you a confirmation email."):
                            send_thank_you_email(email, username, password, job_role, item, place_name)
                    else:
                        st.error('Username already exists. Please try again.')
                        tts('Username already exists. Please try again.')
#############################################################################
#login 
def login(item):
    conn = sqlite3.connect('Data/database.db')
    c = conn.cursor()
    st.markdown(f"<h2 style='text-align: center;color:white'>Log in Here 👇 for {item} Management</h2>", unsafe_allow_html=True)
    with st.form(key="login_form", clear_on_submit=True):
        username = st.text_input("Enter your username")
        password = st.text_input("Enter your password", type="password")
        login_button = st.form_submit_button("Login")
        forgot_password_button = st.form_submit_button("Forgot Password")
        
        if forgot_password_button:
            if username:
                c.execute('SELECT email FROM users WHERE username = ? AND item = ?', (username, item))
                user_data = c.fetchone()
                if user_data:
                    email = user_data[0]
                    new_password = generate_custom_password()
                    c.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
                    conn.commit()
                    send_password_reset_email(email, new_password)
                else:
                    st.error("Username not found.")
                    tts("Username not found.")
            else:
                st.error("Please enter your username.")
                tts("Please enter your username.")
        
        if login_button:
            if not username or not password:
                st.error("Please enter both username and password.")
                tts("Please enter both username and password.")
            else:
                c.execute('SELECT * FROM users WHERE username = ? AND password = ? AND item = ?', (username, password, item))
                if c.fetchone():
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.item = item
                    st.session_state.password = password
                    st.session_state.page = "Dashboard"
                    st.success(f"Welcome back, {username}! You have successfully logged in. Enjoy managing your {item}.")
                    tts(f"Welcome back, {username}! You have successfully logged in. Enjoy managing your {item}.")
                    st.rerun()
                else:
                    tts('Invalid username or password. Please try again.')
                    st.error('Invalid username or password. Please try again.')

def generate_custom_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def send_password_reset_email(email, new_password):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = st.secrets["smtp"]["username"]
        smtp_password = st.secrets["smtp"]["password"]
        
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Password Reset Request'
        
        html = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h1 style="color: #1a73e8; text-align: center;">Password Reset Successful</h1>
            <p>Dear User,</p>
            <p>We are pleased to inform you that your password has been successfully reset. Your new password is:</p>
            <h2 style="color: #333; text-align: center;"><strong>{new_password}</strong></h2>
            <p>Please use this new password to log in to your account. For security reasons, we recommend that you change your password immediately after logging in.</p>
            <p>If you did not request this password reset, please contact our support team immediately to secure your account.</p>
            <p>Best regards,<br>The Support Team</p>
            </div>
        </body>
        </html> 
        """
        message.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        
        tts(f"A new password has been sent to {email}.")
        st.success(f"A new password has been sent to {email}.")
    
    except Exception as e:
        tts(f"Failed to send email: {e}")
        st.error(f"Failed to send email: {e}")
#####################################################################
#changer username
def change_username():
    conn = sqlite3.connect('Data/database.db')
    c = conn.cursor()

    try:
        current_username = st.session_state.username
        showing_username = st.text_input("showing current username",value=current_username,disabled=True)
        new_username = st.text_input("Enter your new username")
        change_username_btn = st.button("Change Username",type="primary")
        
        if change_username_btn:
            if new_username:
                c.execute('SELECT email, job_role FROM users WHERE username = ?', (current_username,))
                user_data = c.fetchone()
                
                if user_data:
                    email, job_role = user_data
                    workplace = st.session_state.item
                    c.execute('SELECT username FROM users WHERE username = ? AND item = ?', (new_username, workplace))
                    if c.fetchone():
                        tts("The new username is already taken within your workplace. Please choose another one.")
                        st.error("The new username is already taken within your workplace. Please choose another one.")
                    else:
                        c.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, current_username))
                        conn.commit()
                        st.session_state.username = new_username
                        tts("Username changed successfully!")
                        st.success("Username changed successfully!")
                        send_username_change_email(email, new_username)
            else:
                tts("New username cannot be empty.")
                st.error("New username cannot be empty.")
    
    except Exception as e:
        tts(f"An error occurred: {e}")
        st.error(f"An error occurred: {e}")
    
    finally:
        conn.close()

def send_username_change_email(email, new_username):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = st.secrets["smtp"]["username"]
        smtp_password = st.secrets["smtp"]["password"]
        
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Username Change Notification'
        
        html = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #1a73e8;">Username Changed Successfully</h1>
                <p>Hello,</p>
                <p>Your username has been successfully changed to <strong>{new_username}</strong>.</p>
                <p>If you did not request this change, please contact our support team immediately.</p>
                <p>Best regards,<br>The Team</p>
            </div>
        </body>
        </html>
        """
        message.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        
        tts(f"A notification email has been dispatched to {email} concerning your username change request.")
        st.success(f"A notification email has been dispatched to {email} concerning your username change request.")
    
    except Exception as e:
        tts(f"Failed to send email: {e}")
        st.error(f"Failed to send email: {e}")
###############################################################################
###############################################################################
#Change Job Role
def change_job_role():
    conn = sqlite3.connect('Data/database.db')
    c = conn.cursor()
    
    try:
        username = st.session_state.username
        c.execute('SELECT job_role, email FROM users WHERE username = ?', (username,))
        user_data = c.fetchone()
        
        if user_data:
            current_job_role, email = user_data
            workplace = st.session_state.item
            if workplace in job_roles:
                roles = job_roles[workplace]
                showing_job = st.text_input("showing current job role",value=current_job_role,disabled=True)
                new_job_role = st.selectbox("Select your new job role", roles)
                
                if st.button("Change Job Role",type="primary"):
                    if new_job_role:
                        c.execute('UPDATE users SET job_role = ? WHERE username = ?', (new_job_role, username))
                        conn.commit()
                        st.session_state.job_role = new_job_role
                        tts("Job role changed successfully!")
                        st.success("Job role changed successfully!")
                        send_job_role_change_email(email, new_job_role)
                    else:
                        tts("Please select a job role.")
                        st.error("Please select a job role.")
            else:
                tts("Invalid workplace.")
                st.error("Invalid workplace.")
    
    except Exception as e:
        tts(f"An error occurred: {e}")
        st.error(f"An error occurred: {e}")
    
    finally:
        conn.close()

def send_job_role_change_email(email, new_job_role):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = st.secrets["smtp"]["username"]
        smtp_password = st.secrets["smtp"]["password"]
        
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Job Role Change Notification'
        
        html = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #1a73e8;">Job Role Changed Successfully</h1>
                <p>Hello,</p>
                <p>Your job role has been successfully changed to <strong>{new_job_role}</strong>.</p>
                <p>If you did not request this change, please contact our support team immediately.</p>
                <p>Best regards,<br>The Team</p>
            </div>
        </body>
        </html>
        """
        message.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        
        tts(f"A notification email has been dispatched to {email} concerning your job role change.")
        st.success(f"A notification email has been dispatched to {email} concerning your job role change request.")
    
    except Exception as e:
        tts(f"Failed to send email: {e}")
        st.error(f"Failed to send email: {e}")
##################################################################################
#################################################################################
#Change Password
def changepass():
    conn = sqlite3.connect('Data/database.db')
    c = conn.cursor()
    
    username = st.session_state.username
    c.execute('SELECT email, password FROM users WHERE username = ?', (username,))
    user_data = c.fetchone()
    
    if user_data:
        email, current_password = user_data
        
        with st.form(key="change_password_form", clear_on_submit=True):
            old_password = st.text_input("Enter your current password", type="password")
            new_password = st.text_input("Enter your new password", type="password")
            confirm_new_password = st.text_input("Confirm your new password", type="password")
            st.caption("New password must be at least 7 characters long and include a combination of uppercase and lowercase letters, numbers, and special characters.")
            change_password = st.form_submit_button("Change Password",type="primary")
            
            if change_password:
                if old_password != current_password:
                    tts("Your current password is incorrect. Please try again.")
                    st.error("Your current password is incorrect. Please try again.")
                elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{7,}$', new_password):
                    tts("New password must be at least 7 characters long and contain a mixture of symbols, capital letters, small letters, and numbers.")
                    st.error("New password must be at least 7 characters long and contain a mixture of symbols, capital letters, small letters, and numbers.")

                elif new_password != confirm_new_password:
                    tts("New password and confirmation do not match. Please try again.")
                    st.error("New password and confirmation do not match. Please try again.")
                else:
                    c.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
                    conn.commit()
                    st.success("Password changed successfully!")
                    send_password_change_email(email)
                    st.session_state.password = new_password
    else:
        tts("User data not found.")
        st.error("User data not found.")
    
    conn.close()

def send_password_change_email(email):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = st.secrets["smtp"]["username"]
        smtp_password = st.secrets["smtp"]["password"]
        
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Password Change Notification'
        
        html = """
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #1a73e8;">Password Changed Successfully</h1>
                <p>Hello,</p>
                <p>Your password has been successfully changed. If you did not request this change, please contact our support team immediately.</p>
                <p>Best regards,<br>The Team</p>
            </div>
        </body>
        </html>
        """
        message.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        
        tts(f"A notification email has been dispatched to {email} concerning your password change request.")
        st.success(f"A notification email has been dispatched to {email} concerning your password change request.")
    
    except Exception as e:
        tts(f"Failed to send email: {e}")
        st.error(f"Failed to send email: {e}")
###############################################################################
#########################################################################
#profile setting
def profilesetting():
    st.markdown(f"<h2 style='text-align: center;color:white'>Profile Setting</h2>", unsafe_allow_html=True)
    selected2 = option_menu(None, ["Change Username", "Update Job Role", "Change Password"], 
    icons=['fill-person-fill', 'bookmark-star', "passport"], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    if selected2 == "Change Username":
        change_username()
    if selected2 == "Update Job Role":
        change_job_role()
    if selected2 == "Change Password":
        changepass()


##########################################################################
#Sign up mail sending
def send_thank_you_email(email, username, password, job_role, item, place_name):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = st.secrets["smtp"]["username"]
        smtp_password = st.secrets["smtp"]["password"]
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Welcome to Our Platform!'
        html = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #1a73e8;">Welcome, {username}!</h1>
                <p>Thank you for registering with us. We're excited to have you on board!</p>
                <p>Your username: <strong>{username}</strong></p>
                <p>Your password: <strong>{password}</strong></p>
                <p>Your job role: <strong>{job_role} in {item}</strong></p>
                <p>Your place of work: <strong>{place_name}</strong></p>
                <p>To get started, you can now log in with your credentials and explore the platform.</p>
                <p>Best regards,<br>The Team</p>
                <hr style="border: 0; border-top: 1px solid #ddd;" />
                <footer>
                    <p style="font-size: 0.9em; color: #777;">
                        &copy; 2024 Our Company IAA. All rights reserved.<br>
                        <a href="http://example.com" style="color: #1a73e8; text-decoration: none;">Visit our website</a>
                    </p>
                </footer>
            </div>
        </body>
        </html>
        """
        message.attach(MIMEText(html, 'html'))
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        st.success(f"Congratulations, {username}! Your registration as a {job_role} in {place_name} is now complete. An email with your login credentials has been sent to {email}. Please check your inbox to access your account and start using our services.")
        tts(f"Congratulations, {username}! Your registration as a {job_role} in {place_name} is now complete. An email with your login credentials has been sent to {email}. Please check your inbox to access your account and start using our services.")
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        tts(f"Failed to send email: {e}")

##################################################################################
##Contact us 
def contact():
    st.markdown(f"<h2 style='text-align: center;color:white'>Contact us</h2>", unsafe_allow_html=True)

    with st.form(key="contact_form", clear_on_submit=True):
        name = st.text_input("Enter your name")
        email = st.text_input("Enter your email address")
        subject = st.text_input("Subject")
        message = st.text_area("Your message")
        submit_button = st.form_submit_button("Send Message")

        if submit_button:
            if not name or not email or not subject or not message:
                st.error("Please fill in all required fields.")
                tts("Please fill in all required fields.")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address.")
                tts("Please enter a valid email address.")
            else:
                send_contact_email(name, email, subject, message)
      
    select = option_menu("MEET OUR TEAM", 
        ['Team','Individual'],
        icons=['people', 'person-bounding-box'],
        menu_icon="microsoft-teams", default_index=0,orientation="horizontal")
    if select == 'Team':
        st.markdown(f"<h2 style='text-align: center;color:white'>Binary Coders</h2>", unsafe_allow_html=True)
        st.balloons()
        st.write("""
        Welcome to the official website of Binary Coders! We are a dynamic team of four passionate tech enthusiasts, united by a shared vision of leveraging technology to solve real-world problems. Our latest project is an innovative attendance and activity detection system designed to streamline processes in hospitals, schools, universities, and offices.
        """)
        st.image('media/team.jpg',use_column_width=True,caption='Team Image')
        # Vision
        st.markdown(f"<h4 style='text-align: center;color:white'>Our Vision</h4>", unsafe_allow_html=True)
        st.write("""
        At Binary Coders, we believe in the transformative power of technology. Our current project aims to revolutionize the way attendance is marked and activities are monitored across various sectors. We are committed to delivering a solution that is not only innovative but also practical and easy to implement. By combining our diverse skill sets, we are creating a system that enhances efficiency, security, and accuracy, all while being user-friendly.
        """)

        # Why Choose Us?
        # st.subheader("Why Choose Us?")
        st.markdown(f"<h4 style='text-align: center;color:white'>Why Choose Us?</h4>", unsafe_allow_html=True)
        st.write("""
        - **Expertise Across Disciplines:** Each member of our team brings a unique set of skills and expertise to the table, ensuring that all aspects of the project are handled with the utmost professionalism.
        - **Innovation-Driven:** We are constantly exploring new technologies and methodologies to improve our solutions, ensuring that our system stays ahead of the curve.
        - **User-Centered Design:** Our focus is always on the end-user. We strive to create systems that are not only powerful but also intuitive and easy to use.
        - **Commitment to Quality:** From the initial concept to the final product, quality is at the heart of everything we do. We are dedicated to delivering solutions that meet the highest standards of excellence.
        """)

        # Closing
       
        st.markdown(f"<h4 style='text-align: center;color:white'>Join Us in Our Journey?</h4>", unsafe_allow_html=True)
        st.write("""
        We invite you to follow our progress as we work to bring this project to life. Whether you're a potential partner, client, or simply someone who shares our passion for technology, we're excited to have you with us on this journey.
        """)
    if select == 'Individual':
        data_df = pd.DataFrame(
        data={
            "Name": ["Sumit Kumar Singh", "Mantu Rana", "Mayank Pathak", "Madan H S"],
            "LinkedIn": [
                "https://www.linkedin.com/in/sumit-singh-773921262/",
                "https://www.linkedin.com/in/mantu-kumar-rana-71a6ba25b/",
                "https://www.linkedin.com/in/mayank-pathak-46168a281/",
                "https://www.linkedin.com/in/madan-hs-491523317/"
            ],
            "GitHub": [
                "https://github.com/RAJPUTRoCkStAr",
                "https://github.com/MantuRana",
                "https://github.com/MayankPathak13/Internship_AI.git",
                "https://github.com/Madanedunet"
            ],
            "apps": [
                "https://raw.githubusercontent.com/RAJPUTRoCkStAr/Human-activity/main/media/sumitimg.jpg",
                "https://raw.githubusercontent.com/RAJPUTRoCkStAr/Human-activity/main/media/resized_mantuimg.jpg",
                "https://raw.githubusercontent.com/RAJPUTRoCkStAr/Human-activity/main/media/resized_mayankimg.jpg",
                "https://raw.githubusercontent.com/RAJPUTRoCkStAr/Human-activity/main/media/resized_madanimg.jpg"
            ]
        }
    )
        st.markdown(f"<h2 style='text-align: center;color:white'>Team Individual Profiles</h2>", unsafe_allow_html=True)
        edited_df = st.data_editor(
        data_df,
        column_config={
            "apps": st.column_config.ImageColumn(
                "Preview Image", help="Streamlit app preview screenshots",width="medium"
            ),
            "LinkedIn": st.column_config.LinkColumn(
                "LinkedIn Profile", help="Edit LinkedIn URL", display_text="LinkedIn Profile"
            ),
            "GitHub": st.column_config.LinkColumn(
                "GitHub Profile", help="Edit GitHub URL", display_text="GitHub Profile"
            )
        },
        hide_index=True,
        use_container_width=True
    )
def send_contact_email(name, email, subject, message):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = st.secrets["smtp"]["username"]
        smtp_password = st.secrets["smtp"]["password"]
        recipient_email = "luciferdevil565656@gmail.com" 

        mail_content = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #1a73e8;">Contact Us Message</h1>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>Message:</strong></p>
                <p>{message}</p>
                <p>Best regards,<br>{name}</p>
            </div>
        </body>
        </html>
        """

        message_obj = MIMEMultipart()
        message_obj['From'] = smtp_username
        message_obj['To'] = recipient_email
        message_obj['Subject'] = subject

        message_obj.attach(MIMEText(mail_content, 'html'))

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message_obj)

        tts("Thank you for contacting us! Your message has been sent successfully.")
        st.success("Thank you for contacting us! Your message has been sent successfully.")

    except Exception as e:
        tts(f"Failed to send email: {e}")
        st.error(f"Failed to send email: {e}")
##################################################################################
#admin login
admin_users = st.secrets["admin"].get("users", [])

def authenticate(username, password):
    for user in admin_users:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def admin_login():
    st.markdown("<h2 style='text-align: center;color:white'>Login for Admin</h2>", unsafe_allow_html=True)
    username = st.text_input("Username",key="username_admin")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state['log_in'] = True
            st.session_state['page'] = "Admin"
            st.session_state['authenticated'] = True
            st.success("Logged in successfully!")
            st.rerun()  
        else:
            st.error("Invalid credentials")
    else:
        st.info("Please log in to see Database")
