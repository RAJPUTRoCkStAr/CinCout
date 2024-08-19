import streamlit as st
from streamlit_option_menu import option_menu
from Attendmain import personadder
from utils import tts,extract_name,profilesetting
import sqlite3
from Manageatten import manageatt
def dashboard():
    with st.sidebar:
        selected = option_menu("Dashboard Menu", 
        ["Profile", 'Manage Attendance', 'ADD', 'Profile Setting', 'Logout'],
        icons=['person-circle', 'clipboard-check', 'person-plus', 'tools', 'box-arrow-right'],
        menu_icon="cast", default_index=0)

    if selected == "Profile":
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        username = st.session_state.username
        name = extract_name(username)
        c.execute('SELECT email, job_role, password, item FROM users WHERE username = ?', (username,))
        user_data = c.fetchone()
        if user_data:
            email, job_role, current_password, work_place = user_data
            st.session_state.work_place = work_place  # Store workplace in session state
            st.header(f"Welcome, {name}!")
            st.write(f"**Username:** {username}")
            st.write(f"**Email:** {email}")
            st.write(f"**Job Role:** {job_role}")
            st.write(f"**Workplace:** {work_place}")
        else:
            st.error("User data not found.")
            tts("User data not found.")
        conn.close()
    elif selected == "Manage Attendance":
        manageatt()
    elif selected == "ADD":
        personadder()
    elif selected == "Profile Setting":
        profilesetting()
    elif selected == "Logout":
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        username = st.session_state.username
        name = extract_name(username)
        tts(f"{name}, you have successfully logged out.")
        st.rerun()

