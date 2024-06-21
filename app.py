import streamlit as st
import pandas as pd
import random
st.set_page_config(page_title='human activity',layout='wide')
col1,col2,col3 = st.columns([2,4,2])
with col1:
    st.image('media/logo.png',width=150)
with col2:
    st.title('Real Time Activity Detection')
with col3:
    login = st.button('login',use_container_width=True,type='primary')
    if login:
        st.write('login button is clicked')


    signup = st.button('signup',use_container_width=True,type='primary')
    if signup:
        st.write('signup button is clicked')

col4,col5 = st.columns([4,2])
with col4:
    st.camera_input('something')
with col5:
    
    data = pd.DataFrame(
         {
        "Activity Name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "Time": [random.randint(0, 1000) for _ in range(3)],
        "Start_time": [[random.randint(0, 5000) for _ in range(30)] for _ in range(1)],
        "End_time/Live": [[random.randint(0, 5000) for _ in range(30)] for _ in range(1))]],
    }
    )
    st.dataframe(data,hide_index=True,use_container_width=True)

col7,col8,col9 = st.columns([2,4,2])
with col7:
    upload = st.button('upload',use_container_width=True,type='primary')
    if upload:
        st.write('upload button clicked')

    monitor = st.button('monitor',use_container_width=True,type='primary')
    if monitor:
        st.write('monitor button clicked',)
with col8:
    notify = st.button('silent notification',use_container_width=True,type='primary')
    if notify:
        st.write('silent notification button clicked')


    loudnotify = st.button('loud notification',use_container_width=True,type='primary')
    if loudnotify:
        st.write('loud notification clicked')
with col9:
    dash = st.button('dashboard',use_container_width=True,type='primary')
    if dash:
        st.write('dashboard button clicked')


    contact_us = st.button('contact us',use_container_width=True,type='primary')
    if contact_us:
        st.write('contact us button clicked')