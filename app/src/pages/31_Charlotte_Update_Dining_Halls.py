import logging
logger = logging.getLogger(__name__)
import datetime
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

BASE_URL = 'http://web-api:4000'
st.title('Dining Hall Management')
st.write('Update Operating Hours & General Info')

# select dining hall
try:
    res = requests.get(f'{BASE_URL}/dininghalls')
    halls = res.json()
    hall_map = {h['Name']: h['HallId'] for h in halls}
except:
    hall_map = {}
    st.error("Couldn't load dining halls from the API.")
    st.stop()

selected = st.selectbox('Select Dining Hall', list(hall_map.keys()))
hall_id  = hall_map[selected]

st.divider()

# turning 24 time to 12 hr am/pm for better UI 
def to_24hr(t):
    return datetime.datetime.strptime(t, '%I:%M %p').strftime('%H:%M:%S')

times = [
    f"{h}:{m:02d} {p}"
    for p in ['AM', 'PM']
    for h in ([12] + list(range(1, 12)))
    for m in [0, 15, 30, 45]
]

# update op hours 
st.write('### Update Operating Hours')
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

col1, col2 = st.columns(2)

with col1:
    
    day_of_week = st.selectbox('Day of Week', days)
    open_time   = st.selectbox('Opening Time', times, key='open')
    close_time  = st.selectbox('Closing Time', times, key='close')

with col2:
    note = st.text_area('Note (optional)', placeholder='e.g. Holiday hours')

    if st.button('Update Hours', type='primary'):
        payload = {
            'OpenTime':  f"{datetime.date.today()} {to_24hr(open_time)}",
            'CloseTime': f"{datetime.date.today()} {to_24hr(close_time)}",
        }
        if note.strip():
            payload['Note'] = note.strip()

        try:
            url = f'{BASE_URL}/dininghalls/{hall_id}/operatinghours/{day_of_week}'
            res = requests.put(url, json=payload)

            if res.status_code == 200:
                st.success(f'Hours updated for {selected} on {day_of_week}!')
            elif res.status_code == 404:
                st.error('No operating hours record found for hall and day.')
            else:
                st.error(f'Something went wrong: {res.json().get("error", res.status_code)}')
        except requests.exceptions.ConnectionError:
            st.error("Couldn't connect to the API.")