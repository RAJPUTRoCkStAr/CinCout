import streamlit as st
import pandas as pd
import numpy as np
from Attendmain import view_attendance
def home():
    view_attendance()
    ma = st.button('Monitor Activity', use_container_width=True, type='primary')
    if ma:
        st.write('Monitor button clicked')

