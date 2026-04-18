import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('Update Dining Halls',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/31_Charlotte_Update_Dining_Halls.py')

if st.button('View Feedback',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Charlotte_View_Student_Feedback.py')

if st.button('Visualizations',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/33_Charlotte_Visualizations.py')   