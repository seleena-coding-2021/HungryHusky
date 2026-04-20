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

dininghalls = requests.get('http://web-api:4000/dininghalls', timeout=10).json()

try:
    st.dataframe(dininghalls, column_order=["Name", "Location", "CampusArea", "Capacity", "HallID" ])
except:
    st.write("Could not connect to database to retrieve restaurants")
    
# view stations
st.subheader("View stations:", divider="gray")

dininghall_items = {d["Name"]: d["HallId"] for d in dininghalls}

selected_hall = st.selectbox("Select a dining hall", list(dininghall_items.keys()))
hall_id = dininghall_items[selected_hall]

stations = requests.get(f'http://web-api:4000/dininghalls/{hall_id}/stations', timeout=10).json()

try:
    st.dataframe(stations, column_order=["StationId", "HallId", "ItemId", "Name", "WaitMinutes", "UpdatedAt" ])
except:
    st.write("Could not connect to database to retrieve stations")
    
# view menu items at dining hall
st.subheader("View dining hall menu items:", divider="gray")

dininghall_items2 = {d["Name"]: d["HallId"] for d in dininghalls}
selected_hall2 = st.selectbox("Select dining hall", list(dininghall_items2.keys()))
hall_id2 = dininghall_items2[selected_hall2]

menu_items = requests.get(f'http://web-api:4000/dininghalls/{hall_id2}/menuitems', timeout=10).json()

try:
    st.dataframe(menu_items, column_order=["ItemId", "ItemName", "Description", "Category", "IsAvailable"])
except:
    st.write("Could not connect to database to retrieve menu items")