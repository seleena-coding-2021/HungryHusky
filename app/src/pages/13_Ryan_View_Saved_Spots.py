import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("Saved Spots")
st.subheader("View Saved Spots", divider="gray")

stu_id = st.number_input("Please enter your student id", min_value=0, step=1)

if stu_id > 0:
    saved_spots = requests.get(f'http://web-api:4000/students/{stu_id}/savedspots', timeout=10).json()

    try:
        st.dataframe(saved_spots, column_order=["RestaurantName", "HallName", "PriceRange", "Cuisine",
        "DateAdded", "Address", "DistFromCampus", "Notes", "SavedId", ])
    except:
        st.write("Could not connect to database to retrieve saved spots")

st.subheader("Delete a saved spot", divider="gray")

stu_id_del = st.number_input("Please enter your student id", min_value=0, step=1, key="del_stu_id")
saved_id = st.number_input("Please enter the SavedId of the spot to delete", min_value=0, step=1, key="del_saved_id")

if stu_id_del > 0 and saved_id > 0:
    if st.button("Delete saved spot"):
        response = requests.delete(f'http://web-api:4000/students/{int(stu_id_del)}/savedspots/{int(saved_id)}', timeout=10)
        if response.status_code == 200:
            st.success("Spot deleted successfully!")
        else:
            st.error("Failed to delete saved spot")