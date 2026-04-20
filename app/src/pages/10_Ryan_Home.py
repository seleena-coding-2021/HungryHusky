import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('### Where would you like to go today?')

if st.button('Restaurants',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_Ryan_View_Restaurants.py')

if st.button('Reviews',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/12_Ryan_View_Reviews.py')

if st.button('Saved Spots',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/13_Ryan_View_Saved_Spots.py')

