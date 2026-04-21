import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
import requests
from datetime import datetime
from datetime import date

st.set_page_config(layout='wide')

SideBarLinks()


st.title("Restaurants")

# all restaurants, filter by distance
st.subheader("Restaurant Filtering", divider="gray")

max_dist = st.selectbox(
    "Filter by distance within range:",
    ["5.0", "4.5", "4.0", "3.5", "3.0", "2.5",
     "2.0", "1.5", "1.0", "0.5", "0.0"]
)

params = {}

if max_dist:
    params["maxDist"] = max_dist


restaurants = requests.get(
        "http://web-api:4000/restaurants/",
        params=params,
        timeout=10
    ).json()
    
try:

    st.dataframe(restaurants, column_order=["Name", "PriceRange","DistFromCampus", "Cuisine",
                                            "Address", "RestaurantId", ])

except requests.exceptions.RequestException:
    st.write("Could not connect to database to retrieve restaurants")
    
#save spot
st.subheader("Saved Spots", divider="gray")

student_id = st.number_input("Please enter your student id", min_value=0, step=1)

if student_id > 0:
    saved_spots = requests.get(f'http://web-api:4000/students/{student_id}/savedspots', timeout=10).json()

    try:
        st.dataframe(saved_spots, column_order=["RestaurantName", "HallName", "PriceRange", "Cuisine",
        "DateAdded", "Address", "DistFromCampus", "Notes", "SavedId", ])
    except:
        st.write("Could not connect to database to retrieve saved spots")


st.subheader("Save a Restaurant", divider="gray")
restaurant_names = {r["Name"]: r["RestaurantId"] for r in restaurants}


select_to_save = st.selectbox("Select a restaurant to save", [""] + list(restaurant_names.keys()))

if select_to_save:
    selected_id = restaurant_names[select_to_save]
    if st.button("Save Spot"):
        response = requests.post(f'http://web-api:4000/restaurants/{selected_id}',
                    json={
                    "RestaurantId": selected_id,
                    "DateAdded": date.today().isoformat(),
                    "studentId": 158088292
                    },
                    headers={"Content-Type": "application/json"}, timeout=10).json()
        if "error" not in response:
            st.success(f"Saved {select_to_save} to your spots!")
        else:
            st.error(response["error"])

st.subheader("View a Wait Time", divider="gray")

view = st.selectbox("Select a restaurant to view a wait time", [""] + list(restaurant_names.keys()))

if view:
    view_id = restaurant_names[view]
    wait_times = requests.get(f'http://web-api:4000/restaurants/restaurant/{view_id}/waittime', timeout=10).json()
    if not wait_times:
        with st.container(border=True):
            st.write(f"No wait times have been posted for {view} yet!")
    if wait_times:
        latest = wait_times[0]
        with st.container(border=True):
            st.subheader(f"**{latest['Name']}**")
            if latest['EstimatedMin']:
                st.write(f"**Most recent wait time (min)**: {latest['EstimatedMin']}")

st.subheader("Add a Wait Time", divider="gray")

with st.container(border=True):
    rest_to_post = st.selectbox("Select a restaurant to post a wait time about", [""] + list(restaurant_names.keys()))
    wait_min = st.selectbox("Wait Time Estimate (min):", ["10", "20", "30", "40", "60", "90", "120"])

if rest_to_post:
    rest_id = restaurant_names[rest_to_post]
    if st.button("Add a wait time estimate"):
        response = requests.post(f'http://web-api:4000/restaurants/restaurant/{rest_id}/waittime',
                    json={
                    "EstimatedMin": wait_min,
                    "TimeStamp": datetime.now().isoformat(),
                    },
                    headers={"Content-Type": "application/json"}, timeout=10).json()
        if "error" not in response:
            st.success("Added your wait time estimate!")
        else:
            st.error(response["error"])
