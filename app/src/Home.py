##################################################
# Home.py
# Main entry point for the HungryHusky application
# users select which persona they want to log in as
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports regular and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout='wide')

# If a user is at this page, we assume they are not
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false.
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel.
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

logger.info("Loading the Home page of the app")
st.title('HungryHusky')
st.write('#### Hi! Which user would you like to log in as?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user
# can click to MIMIC logging in as that mock user.

# ***************************************************
#    Persona 1: Alex Smith -- Freshman with Nut Allergy
# ***************************************************

if st.button("Act as Alex, Freshman Student",
             type='primary',
             use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'student_alex'
    # we add the first name of the user (so it can be displayed on
    # subsequent pages).
    st.session_state['first_name'] = 'Alex'
    st.session_state['student_id'] = 158088292
    # finally, we ask streamlit to switch to another page, in this case, the
    # landing page for this particular user type
    logger.info("Logging in as Alex (Freshman Student)")
    st.switch_page('pages/00_Alex_Home.py')

# ***************************************************
#    Persona 2: Ryan Jacob -- Senior Off-Campus Student
# ***************************************************
    
if st.button('Act as Ryan, a Senior Student',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'student_ryan'
    st.session_state['first_name'] = 'Ryan'
    st.session_state['student_id'] = 190378124
    logger.info("Logging in as Ryan (Senior Student)")
    st.switch_page('pages/10_Ryan_Home.py')

# ***************************************************
#    Persona 3: Mary Johnson - Campus Dining Services Manager
# ***************************************************
if st.button('Act as Mary, a Dining Services Manager',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'dining_manager'
    st.session_state['first_name'] = 'Mary'
    st.session_state['admin_id'] = 2
    logger.info("Logging in as Mary (Dining Services Manager)")
    st.switch_page('pages/20_Mary_Home.py')

# ***************************************************
# Persona 4: Dr. Charlotte Garcia — Director of Campus Food Services
# ***************************************************
if st.button("Act as Dr. Garcia, Director of Campus Food Services",
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'director'
    st.session_state['first_name'] = 'Charlotte'
    st.session_state['admin_id'] = 1
    logger.info("Logging in as Dr. Garcia (Director)")
    st.switch_page('pages/30_Charlotte_Home.py')