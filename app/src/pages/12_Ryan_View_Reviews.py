import logging
logger = logging.getLogger(__name__)
from datetime import date

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Reviews")
st.subheader("View Reviews", divider="gray")

rest_id = st.number_input("Enter the id of the **restaurant** whose reviews you'd like to view",
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
    review_type = st.radio("What are you reviewing?*", ["Restaurant", "Dining Hall"])
    stu_id = st.number_input("Student id*", min_value=0, step=1, key="stu_id")
    rating = st.radio("Rating*", [1, 2, 3, 4, 5])
    comment = st.text_input("Comments?")
    price_rating = st.radio("Price Rating", ["", 1, 2, 3, 4, 5])
    allergen_flag = st.text_input("Allergen flags?")

    if review_type == "Restaurant":
        rest_id = st.number_input("Please input the id of the restaurant you'd like to review",
                                    min_value=0, step=1, key="rest_id")

        if stu_id > 0 and rest_id > 0 and rating > 0:
            if st.button("Add a review"):
                response = requests.post(f'http://web-api:4000/restaurants/{int(rest_id)}/reviews',
                            json={
                            "studentId": stu_id,
                            "rating": rating,
                            "comment": comment,
                            "allergenFlag": allergen_flag,
                            "priceRating": price_rating,
                            "reviewDate": date.today().isoformat()
                            },
                            headers={"Content-Type": "application/json"}, timeout=10).json()
                if "error" not in response:
                    st.success("Added review successfully!")
                else:
                    st.error(response["error"])
    else:
        dh_id = st.number_input("Please input the id of the dining hall you'd like to review",
                                min_value=0, step=1, key="dh_id")
        if stu_id > 0 and dh_id > 0:
            if st.button("Add a review"):
                response = requests.post(f'http://web-api:4000/student/{int(stu_id)}/review',
                json={
                    "studentId": stu_id,
                    "rating": rating,
                    "comment": comment,
                    "allergenFlag": allergen_flag,
                    "priceRating": price_rating,
                    "ReviewDate": date.today().isoformat()
                }, headers={"Content-Type": "application/json"}, timeout=10)
                if "error" not in response:
                    st.success("Added review successfully!")
                else:
                    st.error(response["error"])

st.subheader("Delete Review", divider="gray")

with st.container(border=True):
    stu_id_del = st.number_input("Please enter your student id", min_value=0, step=1, key="del_stu_id")
    review_id = st.number_input("Please enter the review id of the review you want to delete",
                                min_value=0, step=1, key="review_id")
    if review_id > 0 and stu_id_del > 0:
        if st.button("Delete a review"):
            response = requests.delete(f'http://web-api:4000/student/{int(stu_id_del)}/reviews/{int(review_id)}', timeout=10)
            if response.status_code == 200:
                st.success("Review deleted successfully!")
            else:
                st.error("Failed to delete review")