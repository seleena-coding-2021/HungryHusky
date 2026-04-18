# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has functions to add links to the left sidebar based on the user's role.

import streamlit as st


# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def about_page_nav():
    st.sidebar.page_link("pages/40_About.py", label="About", icon="🧠")


# ---- Role: student_alex (persona 1) ------------------------------------------------

def alex_home_nav():
    st.sidebar.page_link("pages/00_Alex_Home.py", label="Alex's Home", icon="👤")
 
def alex_dining_halls_nav():
    st.sidebar.page_link("pages/01_Alex_View_Dining_Hall.py", label="Dining Halls", icon="🍽️")
 
def alex_restaurants_nav():
    st.sidebar.page_link("pages/02_Alex_View_Restaurants.py", label="Restaurants", icon="🍜")
 
def alex_feedback_nav():
    st.sidebar.page_link("pages/03_Alex_Submit_Feedback.py", label="Feedback", icon="📝")
 
def alex_allergen_profile_nav():
    st.sidebar.page_link("pages/04_Alex_Allergen_Profile.py", label="Allergen Profile", icon="⚠️")

# ---- Role: student_ryan (persona 2) -----------------------------------------------------

def ryan_home_nav():
    st.sidebar.page_link("pages/10_Ryan_Home.py", label="Ryan's Home", icon="👤")
 
def ryan_restaurants_nav():
    st.sidebar.page_link("pages/11_Ryan_View_Restaurants.py", label="Restaurants", icon="🍜")
 
def ryan_reviews_nav():
    st.sidebar.page_link("pages/12_Ryan_View_Reviews.py", label="Reviews", icon="⭐")
 
def ryan_saved_spots_nav():
    st.sidebar.page_link("pages/13_Ryan_View_Saved_Spots.py", label="Saved Spots", icon="🔖")


# ---- Role: dining_manager (persona 3) ----------------------------------------------------

def mary_home_nav():
    st.sidebar.page_link("pages/20_Mary_Home.py", label="Mary's Home", icon="👤")
 
def mary_update_dining_halls_nav():
    st.sidebar.page_link("pages/21_Mary_Update_Dining_Halls.py", label="Update Dining Halls", icon="🏫")
 
def mary_view_feedback_nav():
    st.sidebar.page_link("pages/22_Mary_View_Student_Feedback.py", label="View Feedback", icon="💬")
 
def mary_update_menus_nav():
    st.sidebar.page_link("pages/23_Mary_Update_Menus.py", label="Update Menus", icon="📋")

# ---- Role: director (Persona 4) --------------------------------------------
 
def charlotte_home_nav():
    st.sidebar.page_link("pages/30_Charlotte_Home.py", label="Dr. Garcia's Home", icon="👤")
 
def charlotte_update_dining_halls_nav():
    st.sidebar.page_link("pages/31_Charlotte_Update_Dining_Halls.py", label="Update Dining Halls", icon="🏫")
 
def charlotte_view_feedback_nav():
    st.sidebar.page_link("pages/32_Charlotte_View_Student_Feedback.py", label="View Feedback", icon="💬")
 
def charlotte_visualizations_nav():
    st.sidebar.page_link("pages/33_Charlotte_Visualizations.py", label="Visualizations", icon="📊")


# ---- Sidebar assembly -------------------------------------------------------
 
def SideBarLinks(show_home=False):
    """
    Renders sidebar navigation links based on the logged-in user's role.
    The role is stored in st.session_state when the user logs in on Home.py.
    """
 
    # Logo at the top of the sidebar on every page
    st.sidebar.image("assets/logo.png", width=150)
 
    # If no one is logged in, send them to the Home (login) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")
 
    if show_home:
        home_nav()
 
    if st.session_state["authenticated"]:
 
        if st.session_state["role"] == "student_alex":
            alex_home_nav()
            alex_dining_halls_nav()
            alex_restaurants_nav()
            alex_feedback_nav()
            alex_allergen_profile_nav()
 
        if st.session_state["role"] == "student_ryan":
            ryan_home_nav()
            ryan_restaurants_nav()
            ryan_reviews_nav()
            ryan_saved_spots_nav()
 
        if st.session_state["role"] == "dining_manager":
            mary_home_nav()
            mary_update_dining_halls_nav()
            mary_view_feedback_nav()
            mary_update_menus_nav()
 
        if st.session_state["role"] == "director":
            charlotte_home_nav()
            charlotte_update_dining_halls_nav()
            charlotte_view_feedback_nav()
            charlotte_visualizations_nav()
 
    # About link appears at the bottom for all roles
    about_page_nav()
 
    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")