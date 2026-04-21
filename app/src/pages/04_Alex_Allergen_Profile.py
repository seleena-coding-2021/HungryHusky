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

st.set_page_config(layout='wide')

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# alllergen profile
st.subheader("Student Allergen Profile", divider="gray")

student_id = st.text_input("Enter a student ID")

# hard coded allergens (we don't have a route)
allergen_options = {
    "Peanuts (severe)": 1,
    "Tree Nuts (severe)": 2,
    "Shellfish (severe)": 3,
    "Fish (moderate)": 4,
    "Milk (moderate)": 5,
    "Eggs (moderate)": 6,
    "Wheat (moderate)": 7,
    "Soy (mild)": 8,
    "Gluten (moderate)": 9,
    "Sesame (severe)": 10,
    "Mustard (mild)": 11,
    "Celery (mild)": 12,
    "Lupin (moderate)": 13,
    "Sulfites (mild)": 14,
    "Mollusks (severe)": 15,
    "Corn (mild)": 16,
    "Latex (moderate)": 17,
    "Sunflower Seeds (mild)": 18,
    "Poppy Seeds (mild)": 19,
    "Garlic (mild)": 20,
    "Onion (mild)": 21,
    "Citrus (mild)": 22,
    "Tomato (mild)": 23,
    "Strawberry (mild)": 24,
    "Kiwi (moderate)": 25,
    "Mango (mild)": 26,
    "Avocado (mild)": 27,
    "Banana (mild)": 28,
    "Red Meat (moderate)": 29,
    "Gelatin (mild)": 30
}

# view allergens
if st.button("View Allergen Profile"):
    if not student_id.strip():
        st.error("Please enter a student ID.")
    else:
        try:
            response = requests.get(
                f"http://web-api:4000/student/{student_id}/allergen-profile",
                timeout=10
            )

            if response.status_code == 200:
                allergens = response.json()

                if allergens:
                    st.success("Allergen profile loaded.")
                    for allergen in allergens:
                        st.write(
                            f"- {allergen['AllergyName']} ({allergen['Severity']})"
                        )
                else:
                    st.info("No allergens found for this student.")

            else:
                st.error(f"Error: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

# update allergens
if student_id.strip():
    try:
        current_response = requests.get(
            f"http://web-api:4000/student/{student_id}/allergen-profile",
            timeout=10
        )

        current_labels = []

        if current_response.status_code == 200:
            current_allergens = current_response.json()

            for allergen in current_allergens:
                label = f"{allergen['AllergyName']} ({allergen['Severity']})"
                if label in allergen_options:
                    current_labels.append(label)

        selected_allergens = st.multiselect(
            "Select allergens for this student",
            list(allergen_options.keys()),
            default=current_labels
        )

        if st.button("Update Allergen Profile"):
            selected_ids = [
                allergen_options[label] for label in selected_allergens
            ]

            payload = {
                "AllergenIds": selected_ids
            }

            try:
                update_response = requests.put(
                    f"http://web-api:4000/student/{student_id}/allergen-profile",
                    json=payload,
                    timeout=10
                )
                st.success("Profile updated successfully")

            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")