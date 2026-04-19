import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

BASE_URL = 'http://web-api:4000'

st.title('Student Feedback')
st.write('Browse and filter feedback submitted by students.')

# getting all dining halls names
try:
    halls = requests.get(f'{BASE_URL}/dininghalls').json()
    hall_map = {h['Name']: h['HallId'] for h in halls}
except:
    hall_map = {}
    st.error("Couldn't load dining halls.")
    st.stop()

# filtering by type of review
col1, col2 = st.columns(2)
status       = col1.selectbox('Filter by status', ['All', 'positive', 'neutral', 'negative'])
hall_options = ['All'] + list(hall_map.keys())
selected     = col2.selectbox('Filter by Dining Hall', hall_options)


params = {}
if status != 'All':
    params['status'] = status
if selected != 'All':
    params['hall_id'] = hall_map[selected]

try:
    res = requests.get(f'{BASE_URL}/admins/feedback', params=params)
    if res.status_code == 200:
        data = res.json()
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.info('No feedback found for those filters.')
    else:
        st.error(f'Error {res.status_code}: {res.json().get("error", "Unknown")}')
except requests.exceptions.ConnectionError:
    st.error("Couldn't connect to the API.")