import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About HungryHusky")

st.markdown(
    """
    This is a demo app for HungryHusky for our Introduction to Databases Class.  
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
