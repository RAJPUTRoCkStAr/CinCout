import streamlit as st
from streamlit_option_menu import option_menu
from utils import tts
import smtplib
import random
import string
import sqlite3
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

load_dotenv()
st.set_page_config(page_title="IAA", layout="wide")

# Database setup
conn = sqlite3.connect('users.db')
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

# Job roles
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

# Utility functions
def generate_username(name):
    base_name = name.lower().replace(' ', '')
    random_suffix = ''.join(random.choices(string.digits, k=4))
    username = f"{base_name}{random_suffix}"
    return username

def send_thank_you_email(email, username, password, job_role, item, place_name):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
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

def signup(item):
    st.header(f"Sign Up for {item} Management", divider="rainbow")
    with st.form("signup_form", clear_on_submit=False):
        name = st.text_input("Enter your name")
        job_role = st.selectbox("Select your job role", job_roles[item])
        place_name = st.text_input(f"Enter your {item.lower()} name")
        email = st.text_input("Enter your email address")
        password = st.text_input("Enter your password", type="password")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            if not name or not email or not password or not place_name:
                st.error("Please fill in all required fields.")
            elif not re.match("^[A-Za-z\s]+$", name):
                st.error("Name should contain only alphabets and spaces.")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address.")
            else:
                c.execute('''
                    SELECT * FROM users 
                    WHERE name = ? AND email = ? AND job_role = ? AND place_name = ? AND item = ?
                ''', (name, email, job_role, place_name, item))
                if c.fetchone():
                    st.error('A user with the same name, email, job role, and place name already exists. Please try again.')
                else:
                    username = generate_username(name)
                    c.execute('SELECT * FROM users WHERE username = ?', (username,))
                    if c.fetchone() is None:
                        c.execute('INSERT INTO users (name, job_role, email, username, password, item, place_name) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                                  (name, job_role, email, username, password, item, place_name))
                        conn.commit()
                        send_thank_you_email(email, username, password, job_role, item, place_name)
                    else:
                        st.error('Username already exists. Please try again.')

def login(item):
    st.subheader("Log in Here 👇", divider='rainbow')
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Enter your username")
        password = st.text_input("Enter your password", type="password")
        re_sub = st.form_submit_button("Submit")
        
        if re_sub:
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                c.execute('SELECT * FROM users WHERE username = ? AND password = ? AND item = ?', (username, password, item))
                if c.fetchone():
                    st.success(f"Welcome back, {username}! You have successfully logged in. Enjoy managing your {item}.")
                    tts(f"Welcome back, {username}! You have successfully logged in. Enjoy managing your {item}.")
                else:
                    st.error('Invalid username or password. Please try again.')

# Main app layout with page navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Home", "Sign Up", "Login", "Contact Us"])

if page == "Home":
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.image('media/logo.png', width=150)
    with col2:
        st.title('IAA')
    with col3:
        st.write("Welcome to IAA. Please select a page from the sidebar.")

elif page == "Sign Up":
    selected = st.sidebar.selectbox("Select Institution", ["School", "University", "Hospital", 'Office'])
    signup(selected)

elif page == "Login":
    selected = st.sidebar.selectbox("Select Institution", ["School", "University", "Hospital", 'Office'])
    login(selected)

elif page == "Contact Us":
    with st.form("contact_form"):
        contact_name = st.text_input("Name")
        contact_email = st.text_input("Email")
        contact_message = st.text_area("Message")
        contact_submit = st.form_submit_button("Send")
        if contact_submit:
            if not contact_name or not contact_email or not contact_message:
                st.error("Please fill in all fields.")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", contact_email):
                st.error("Please enter a valid email address.")
            else:
                st.success(f"Thank you, {contact_name}! Your message has been sent.")
