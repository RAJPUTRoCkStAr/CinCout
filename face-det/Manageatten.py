import streamlit as st
from streamlit_option_menu import option_menu
from Attendmain import view_attendance,view_registered_persons,cleardatabase,search_attendance,clearrecenthistory
def manageatt():
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