import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('Dining Halls',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_Alex_View_Dining_Hall.py')

if st.button('Restaurants',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_Alex_View_Restaurants.py')

if st.button('Feedback',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_Alex_Submit_Feedback.py')

if st.button('Allergen Profile',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/04_Alex_Allergen_Profile.py')   