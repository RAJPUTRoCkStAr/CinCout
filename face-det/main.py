import streamlit as st
from streamlit_option_menu import option_menu
from utils import tts, generate_username, send_thank_you_email
import re
import sqlite3
from dash import dashboard


st.set_page_config(page_title="IAA", layout="wide")


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

def signup(item):
    st.header(f"Sign Up for {item} Management")
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
            elif not re.match("^[A-Za-z\s]+$", name):
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
                        send_thank_you_email(email, username, password, job_role, item, place_name)
                        st.success('Sign up successful!')
                        tts('Sign up successful!')
                    else:
                        st.error('Username already exists. Please try again.')
                        tts('Username already exists. Please try again.')

def login(item):
    st.subheader(f"Log in Here 👇 for {item} Management")
    with st.form(key="login_form", clear_on_submit=True):
        username = st.text_input("Enter your username")
        password = st.text_input("Enter your password", type="password")
        re_sub = st.form_submit_button("Login")
        
        if re_sub:
            if not username or not password:
                st.error("Please enter both username and password.")
                tts("Please enter both username and password.")
            else:
                c.execute('SELECT * FROM users WHERE username = ? AND password = ? AND item = ?', (username, password, item))
                if c.fetchone():
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.item = item
                    st.session_state.page = "Dashboard" 
                    st.success(f"Welcome back, {username}! You have successfully logged in. Enjoy managing your {item}.")
                    tts(f"Welcome back, {username}! You have successfully logged in. Enjoy managing your {item}.")
                    st.rerun()  
                else:
                    st.error('Invalid username or password. Please try again.')
                    tts('Invalid username or password. Please try again.')


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Home"


if st.session_state.logged_in:
    dashboard()
else:
    with st.sidebar:
        st.session_state.page = option_menu("Main Menu", ["Home", "Sign Up", "Login", "Contact Us"], 
        icons=['house', 'door-open','box-arrow-in-right','person-rolodex'], menu_icon="cast", default_index=0)
    
    if st.session_state.page == "Home":
        col1, col2, col3 = st.columns([2, 4, 2])
        with col1:
            st.image('media/logo.png', width=150)
        with col2:
            st.title('IAA')
        with col3:
           st.empty()

    elif st.session_state.page == "Sign Up":
        selected = st.sidebar.selectbox("Select Institution", ["School", "University", "Hospital", 'Office'])
        signup(selected)

    elif st.session_state.page == "Login":
        selected = st.sidebar.selectbox("Select Institution", ["School", "University", "Hospital", 'Office'])
        login(selected)

    elif st.session_state.page == "Contact Us":
        with st.form("contact_form", clear_on_submit=True):
            contact_name = st.text_input("Enter your name")
            contact_email = st.text_input("Enter your email address")
            contact_message = st.text_area("Enter your message")
            contact_submit = st.form_submit_button("Send Message")
            if contact_submit:
                if not contact_name or not contact_email or not contact_message:
                    st.error("Please fill in all required fields.")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", contact_email):
                    st.error("Please enter a valid email address.")
                else:
                    st.success(f"Thank you, {contact_name}! Your message has been sent.")
