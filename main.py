from streamlit_option_menu import option_menu
from Utils import title,contact,login,signup,admin_login
from PeopleCount import peoplecounter
from Attendmain import search_attendance
from Attendan import atten
from Dashboard import dashboard
from Admin import view_database
import streamlit as st
title()


# query_params = st.experimental_get_query_params()

# url_page = query_params.get("page", ["home"])[0]

# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False

# if url_page == "admin":
#     admin_login()
#     if st.session_state.log_in:
#         view_database()
#         st.rerun()


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if st.session_state.logged_in:
    dashboard()

if 'log_in' not in st.session_state:
    st.session_state.log_in = False
if 'pag' not in st.session_state:
    st.session_state.pag = "Home"
if st.session_state.log_in:
    view_database()
else:
    with st.sidebar:
        st.session_state.page = option_menu(
    "Main Menu",
    ["Monitor", "Attendance", "Search Attendance", "Sign Up", "Login", "Contact Us","Admin"], 
   icons = [
    'eye-fill',        # Monitor
    'check2-square',   # Attendance
    'search',          # Search Attendance
    'person-plus',     # Sign Up
    'person-lock',     # Login
    'envelope',        # Contact Us
    'gear'             # Admin
    ], 
    menu_icon="menu-up", 
    default_index=0,
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
    elif st.session_state.page == "Admin":
        admin_login()
