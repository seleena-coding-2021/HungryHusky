import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime, date, time

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Update Dining Hall Operating Hours')

hall_id = st.number_input('Dining Hall ID', min_value=1, step=1, value=1)

st.write('#### Select Day of Week and New Hours')

day_of_week = st.selectbox('Day of Week', [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
])

open_time = st.time_input('Opening Time', value=time(8,0))
close_time = st.time_input('Closing Time', value=time(21,30))

note = st.text_input('Note (optional)', placeholder='e.g. Holiday hours')

if st.button('Update Hours', type='primary', use_container_width=True):
    payload = {
        'OpenTime': datetime.combine(date.today(), open_time).strftime('%Y-%m-%d %H:%M:%S'),
        'CloseTime': datetime.combine(date.today(), close_time).strftime('%Y-%m-%d %H:%M:%S'),
    }
    if note:
        payload['Note'] = note

    response = requests.put(
        f'http://web-api:4000/dininghalls/{int(hall_id)}/operatinghours/{day_of_week}',
        json=payload
    )

    if response.status_code == 200:
        st.success(f'Hours updated for Hall {int(hall_id)} on {day_of_week}.')
    elif response.status_code == 404:
        st.error(f'No record found for Hall {int(hall_id)} on {day_of_week}.')
    else:
        st.error(f'Error {response.status_code}: {response.text}')