import streamlit as st
import pandas as pd
import numpy as np
def monitor():
    ma = st.button('Monitor Activity', use_container_width=True, type='primary')
    if ma:
        st.write('Monitor button clicked')

