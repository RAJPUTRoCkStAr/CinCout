# from streamlit_option_menu import option_menu
# from Utils import title, contact, login, signup, admin_login
# from PeopleCount import peoplecounter
# from Attendmain import search_attendance
# from Attendan import atten
# from Dashboard import dashboard
# from Admin import view_database
# import streamlit as st


# title()


# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False  
# if 'log_in' not in st.session_state:
#     st.session_state.log_in = False  

# if st.session_state.logged_in:
#     dashboard()  
# elif st.session_state.log_in:
#     view_database()   


# if not st.session_state.logged_in and not st.session_state.log_in:
#     with st.sidebar:
#         app = option_menu(
#             "Main Menu",
#             ["Monitor", "Attendance", "Search Attendance", "Sign Up", "Login", "Contact Us", "Admin"], 
#             icons=[
#                 'eye-fill',        # Monitor
#                 'check2-square',   # Attendance
#                 'search',          # Search Attendance
#                 'person-plus',     # Sign Up
#                 'person-lock',     # Login
#                 'envelope',        # Contact Us
#                 'gear'             # Admin
#             ],
#             menu_icon="menu-up", 
#             default_index=0,
#         )

#     # Handle app navigation
#     if app == "Monitor":
#         peoplecounter()

#     elif app == "Attendance":
#         atten()

#     elif app == "Search Attendance":
#         search_attendance()

#     elif app == "Sign Up":
#         selected = st.sidebar.selectbox("Select Institution", ["School", "University", "Hospital", 'Office'])
#         signup(selected)

#     elif app == "Login":
#         selected = st.sidebar.selectbox("Select Institution", ["School", "University", "Hospital", 'Office'])
#         login(selected)

#     elif app == "Contact Us":
#         contact()

#     elif app == "Admin":
#         admin_login()
#         if st.session_state.log_in:
#             st.rerun()  # Once admin is logged in, reload the page