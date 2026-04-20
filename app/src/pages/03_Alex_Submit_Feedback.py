import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests
from datetime import date

st.set_page_config(layout='wide')

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Dining Hall Feedback')
st.write("Give feedback for dining halls!")

halls = requests.get("http://web-api:4000/dininghalls", timeout=10).json()
hall_options = {hall["Name"]: hall["HallId"] for hall in halls}

selected_hall_name = st.selectbox("Select a dining hall",list(hall_options.keys()))

student_id = st.number_input("Enter student ID")

dietary_restriction = st.selectbox(
    "Dietary restriction",
    [
        "vegan", "vegetarian", "pescatarian", "gluten-free",
        "halal", "kosher", "dairy-free", "nut-free", "egg-free"
    ],
    key="feedback_diet"
)

status = st.selectbox(
    "Feedback status",
    ["positive", "negative", "neutral"],
    key="feedback_status"
)

cuisine_pref = st.selectbox(
    "Cuisine preference (optional)",
    ["", "italian", "chinese", "mexican", "mediterranean", "indian", "fusion", "american", "other"],
    key="feedback_cuisine"
)

content = st.text_area("Feedback comments", key="feedback_content")
submitted_date = st.date_input("Submitted date", value=date.today(), key="feedback_date")

if st.button("Submit Dining Hall Feedback"):
    payload = {
        "StudentId": int(student_id),
        "DietaryRestriction": dietary_restriction,
        "SubmittedDate": str(submitted_date),
        "Status": status
    }

    if cuisine_pref:
        payload["CuisinePref"] = cuisine_pref

    if content:
        payload["Content"] = content

    try:
        res = requests.post(
            f"http://web-api:4000/dininghalls/{hall_id}/studentfeedback",
            json=payload,
            timeout=10
        )

    except requests.exceptions.RequestException:
        st.error("Could not connect to database to submit feedback")