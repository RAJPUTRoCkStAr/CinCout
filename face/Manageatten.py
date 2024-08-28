import streamlit as st
from streamlit_option_menu import option_menu
from utils import extract_name
import sqlite3
from Attendmain import view_attendance,view_registered_persons,cleardatabase,search_attendance,clearrecenthistory
def manageatt():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    username = st.session_state.username
    name = extract_name(username).capitalize()
    c.execute('SELECT email, job_role, password, item FROM users WHERE username = ?', (username,))
    user_data = c.fetchone()
    st.markdown(f"<h2 style='text-align: center;color:green'>Welcome {name}</h2>", unsafe_allow_html=True)
    select = option_menu(None, ["Registered person", "Recent Attendance","Search Attendance"], 
        icons=['people','clipboard-pulse','search'], orientation="horizontal",menu_icon="cast", default_index=0)
    if select == "Registered person":
        view_registered_persons()
        if st.button("Delete database",use_container_width=True,type='primary'):
            cleardatabase()
    elif select == "Recent Attendance":
        view_attendance()
        if st.button('Clear Recent Data',use_container_width=True,type='primary'):
            clearrecenthistory()
    elif select == "Search Attendance":
        search_attendance()