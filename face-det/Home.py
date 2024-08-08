import streamlit as st
import pandas as pd
import numpy as np
from Attendmain import Takeattendance,view_attendace,clearthing
def home():
    Takeattendance()
    view_attendace()
    upload = st.button('Upload Activity Image',use_container_width=True,type='primary')
    if upload:
        st.write('upload button clicked')

    monitor = st.button('Monitor Activity',use_container_width=True,type='primary')
    if monitor:
        st.write('monitor button clicked',)

