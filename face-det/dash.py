import streamlit as st
from streamlit_option_menu import option_menu
from Attendmain import view_attendace,personadder,cleardatabase,clearrecenthistory
from utils import tts,extract_name,profilesetting
import sqlite3
def dashboard():
    with st.sidebar:
        selected = option_menu("Dashboard Menu", 
        ["Profile", 'Attendance History', 'Manage Attendance','ADD','Profile Setting','Logout'],
        icons=['person-circle', 'clipboard2-data', 'gear', 'file-plus','gear-wide-connected',
        'box-arrow-in-right'],menu_icon="cast", default_index=0)
    if selected == "Profile":
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        username = st.session_state.username
        name = extract_name(username)
        c.execute('SELECT email, job_role, password FROM users WHERE username = ?', (username,))
        user_data = c.fetchone()
        if user_data:
            email, job_role, current_password = user_data
            st.header(f"Welcome, {name}!")
            st.subheader("Your Profile Information")
            st.write(f"**Username:** {username}")
            st.write(f"**Email:** {email}")
            st.write(f"**Job Role:** {job_role}")
        else:
            st.error("User data not found.")
            tts("User data not found.")
        conn.close()
    elif selected == "Attendance History":
        view_attendace()
        if st.button("Delete database:"):
            cleardatabase()
        if st.button("clear Recent:"):
            pass
            clearrecenthistory()
    elif selected == "Manage Attendance":
        pass
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

