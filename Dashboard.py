from Utils import tts,extract_name,profilesetting
from streamlit_option_menu import option_menu
from Attendmain import personadder
from Manageatten import manageatt
import streamlit as st
import sqlite3
def dashboard():

    with st.sidebar:
        selected = option_menu("Dashboard Menu", 
        ['Manage Attendance', 'ADD', 'Profile Setting', 'Logout'],
        icons=['clipboard-check', 'person-plus', 'file-person', 'box-arrow-right'],
        menu_icon="cast", default_index=0)
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        username = st.session_state.username
        name = extract_name(username)
        c.execute('SELECT email, job_role, password, item FROM users WHERE username = ?', (username,))
        user_data = c.fetchone()
        if user_data:
            email, job_role, current_password, work_place = user_data
            st.session_state.work_place = work_place
            st.markdown(f"<h2 style='text-align: center;'>Personal Information</h2>", unsafe_allow_html=True)
            st.markdown("<hr style='border-top: 2px solid #bbb;'>", unsafe_allow_html=True)
            st.markdown(f"**👤 Username:** `{username}`")
            st.markdown(f"**📧 Email:** `{email}`")
            st.markdown(f"**💼 Job Role:** `{job_role}`")
            st.markdown(f"**🏢 Workplace:** `{work_place}`")
            st.markdown("<hr style='border-top: 2px solid #bbb;'>", unsafe_allow_html=True)
        else:
            st.error("User data not found.")
            tts("User data not found.")
        conn.close()

    if selected == "Manage Attendance":
        manageatt()
    elif selected == "ADD":
        st.markdown(f"<h2 style='text-align: center;color:green'>Register a person for Attendance</h2>", unsafe_allow_html=True)
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

