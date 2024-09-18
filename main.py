import streamlit as st
from streamlit_option_menu import option_menu
from Utils import title, contact, login, signup, admin_login
from PeopleCount import peoplecounter
from Attendmain import search_attendance
from Attendan import atten
from Dashboard import dashboard
from Admin import view_database
title()

query_params = st.experimental_get_query_params()
page = query_params.get("page", ["home"])[0]
admin_code = query_params.get("admin_code", [None])[0]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False
if 'log_in' not in st.session_state:
    st.session_state.log_in = False

if admin_code == "2261331":
    st.session_state.admin_mode = True

if st.session_state.admin_mode:
    if not st.session_state.log_in:
        admin_login()  
        if st.session_state.log_in:
            st.experimental_set_query_params(admin_code="456", page="view_database")
            st.experimental_rerun()  
    else:
        view_database()  
        st.stop()  

if st.session_state.logged_in:
    dashboard()  
    st.stop()  

if not st.session_state.logged_in and not st.session_state.admin_mode:
    with st.sidebar:
        app = option_menu(
            "Main Menu",
            ["Monitor", "Attendance", "Search Attendance", "Sign Up", "Login", "Contact Us"], 
            icons=[
                'eye-fill',        # Monitor
                'check2-square',   # Attendance
                'search',          # Search Attendance
                'person-plus',     # Sign Up
                'person-lock',     # Login
                'envelope'         # Contact Us
            ],
            menu_icon="menu-up", 
            default_index=0,
        )

    if app == "Monitor":
        peoplecounter()
    elif app == "Attendance":
        atten()
    elif app == "Search Attendance":
        search_attendance()
    elif app == "Sign Up":
        selected = st.sidebar.selectbox("Select Institution", ["School", "University", "Hospital", 'Office'])
        signup(selected)
    elif app == "Login":
        selected = st.sidebar.selectbox("Select Institution", ["School", "University", "Hospital", 'Office'])
        login(selected)
    elif app == "Contact Us":
        contact()
