import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import date, datetime

st.set_page_config(layout='wide')

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Dining Halls')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

st.subheader("View dining halls below:", divider="gray")

# get the countries from the world bank data
dininghalls = requests.get('http://web-api:4000/dininghalls', timeout=10).json()

try:
    st.dataframe(dininghalls, column_order=["Name", "Location", "CampusArea", "Capacity", "HallID" ])
except:
    st.write("Could not connect to database to retrieve restaurants")