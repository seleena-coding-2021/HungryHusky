import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Reviews")
st.subheader("View Reviews", divider="gray")

rest_id = st.number_input("Enter the id of the restaurant whose reviews you'd like to view",
                             min_value=0, step=1)

if rest_id > 0:
    reviews = requests.get(f"http://web-api:4000/restaurants/{int(rest_id)}/reviews",
                             timeout=10).json()
    if not reviews:
        with st.container(border=True):
            st.write(f"No reviews have been posted for restaurant id: {rest_id} yet!")
    if reviews:
        try:
            st.dataframe(reviews)
        except:
            st.write("Could not connect to the database to retrieve reviews")

st.subheader("Post a Review", divider="gray")

with st.container(border=True):
    stu_id = st.number_input("Please input your student id", min_value=0, step=1, key="stu_id")
    rest_id = st.number_input("Please input the id of the restaurant you'd like to review",
                                min_value=0, step=1, key="rest_id")
    rating = st.number_input("Please enter your rating (1-5)", min_value=1, max_value=5, step=1)

if stu_id > 0 and rest_id > 0 and rating > 0:
    if st.button("Add a review"):
        response = requests.post(f'http://web-api:4000/restaurants/{rest_id}/reviews',
                    json={
                    "studentId": stu_id,
                    "rating": rating,
                    },
                    headers={"Content-Type": "application/json"}, timeout=10).json()
        if "error" not in response:
            st.success("Added review successfully!")
        else:
            st.error(response["error"])