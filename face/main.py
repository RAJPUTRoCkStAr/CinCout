import streamlit as st
from streamlit_option_menu import option_menu
from utils import title,contact,login,signup
from dash import dashboard
from peoplecount import peoplecounter
from Attendan import atten
from Attendmain import search_attendance
title()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if st.session_state.logged_in:
    dashboard()
else:
    with st.sidebar:
        st.session_state.page = option_menu(
    "Main Menu",
    ["Monitor", "Attendance", "Search Attendance", "Sign Up", "Login", "Contact Us"], 
    icons=['eye-fill', 'check2-square', 'search', 'plus-square', 'door-open', 'info-circle'], 
    menu_icon="menu-up", 
    default_index=0
)
    
    if st.session_state.page == "Monitor":
        peoplecounter()
    if st.session_state.page == "Attendance":
        atten()
    if st.session_state.page == "Search Attendance":
        search_attendance()

    elif st.session_state.page == "Sign Up":
        selected = st.sidebar.selectbox("Select Institution", ["School", "University", "Hospital", 'Office'])
        signup(selected)

    elif st.session_state.page == "Login":
        selected = st.sidebar.selectbox("Select Institution", ["School", "University", "Hospital", 'Office'])
        login(selected)
  
    elif st.session_state.page == "Contact Us":
        contact()
