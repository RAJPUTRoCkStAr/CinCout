import streamlit as st
from streamlit_option_menu import option_menu
from Attendmain import view_attendace,personadder,clearthing
from utils import tts
def dashboard():
    st.header(f"Dashboard for {st.session_state.item} Management")
    st.subheader(f"Welcome  {st.session_state.username}")
    with st.sidebar:
        selected = option_menu("Dashboard Menu", 
        ["Profile", 'Attendance History', 'Manage Attendance','ADD','Logout'],
        icons=['person-circle', 'clipboard2-data', 'gear', 'file-plus',
        'box-arrow-in-right'],menu_icon="cast", default_index=0)
    if selected == "Profile":
        pass
    elif selected == "Attendance History":
        view_attendace()
        if st.button("Delete database:"):
            clearthing()
    elif selected == "Manage Attendance":
        pass
    elif selected == "ADD":
        personadder()
    elif selected == "Logout":
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        tts(f"Logging you out {st.session_state.username}")
        st.rerun()

