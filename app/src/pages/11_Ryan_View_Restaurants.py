import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("Restaurants")
st.subheader("Restaurant Filtering", divider="gray")

# create a 2 column layout
#col1, col2 = st.columns(2)

# add one number input for variable 1 into column 1
#with col1:
#    var_01 = st.number_input("Variable 01:", step=1)

# add another number input for variable 2 into column 2
#with col2:
#    var_02 = st.number_input("Variable 02:", step=1)

# add a button to use the values entered into the number field to send to the
# prediction function via the REST API
#if st.button("Calculate Prediction", type="primary", use_container_width=True):
#    logger.info(f"var_01 = {var_01}, var_02 = {var_02}")
#    results = requests.get(f"http://web-api:4000/prediction/{var_01}/{var_02}")
#    json_results = results.json()
#    st.dataframe(json_results)

cuisine = st.selectbox("Filter by cuisine:",
                           ["", "Italian", "American", "Chinese", "Mexican",
                            "Mediterranean", "Indian", "Fusion", "Other"])

price = st.selectbox("Filter by price:",
                     ["", "$", "$$", "$$$", "$$$$"])

max_dist = st.selectbox("Filter by distance (mi):",
                        ["5.0", "4.5", "4.0", "3.5", "3.0", "2.5",
                        "2.0", "1.5", "1.0", "0.5", "0.0"])

params = {}

if cuisine:
    params["cuisine"] = cuisine
if price:
    params["price"] = price
if max_dist:
    params["maxDist"] = max_dist

restaurants = requests.get('http://web-api:4000/restaurants/', params=params, timeout=10).json()

try:
    st.dataframe(restaurants, column_order=["Name", "PriceRange","DistFromCampus", "Cuisine",
                                            "Address", ])
except:
    st.write("Could not connect to database to retrieve restaurants")

st.subheader("Restaurant Details", divider="gray")