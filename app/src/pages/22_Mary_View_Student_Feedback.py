import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')

SideBarLinks()

st.title('View Student Feedback')

st.write('##### All feedback submitted by students through the app will appear here.')

#filters by feedback (positive, neg, neutral) and by dining hall

col1, col2 = st.columns(2) 
with col1:
    status_filter = st.selectbox('Filter by Status', ['All', 'positive', 'negative', 'neutral'])
with col2:
    hall_filter = st.number_input('Filter by Hall ID (0 = all)', min_value=0, step=1, value=0)

params = {}
if status_filter != 'All':
    params['status'] = status_filter
if hall_filter > 0:
    params['hall_id'] = hall_filter

feedback_response = requests.get('http://web-api:4000/admins/feedback', params=params)

if feedback_response.status_code == 200:
    feedback = feedback_response.json()
    if feedback:
        df = pd.DataFrame(feedback)

        #creates a bar chart to show breakdown of feedback by status if the Status column is present in the response
        if 'Status' in df.columns:
            st.write('### Feedback Breakdown')
            status_counts = df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            st.bar_chart(status_counts.set_index('Status'))

        #table of all feedback
        st.write('##### All Feedback')
        st.dataframe(df, use_container_width=True)
    else:
        st.info('No feedback found.')
else:
    st.error(f'Error {feedback_response.status_code}: {feedback_response.text}')

st.divider()


#updating/del feedback status 
st.write('### Feedback Management')
st.write('##### Update Feedback')

feedback_id = st.number_input('Feedback ID to Update', min_value=1, step=1, value=1)
new_status = st.selectbox('New Status', ['positive', 'negative', 'neutral'])
new_content = st.text_area('Update Content (optional)', placeholder='Leave blank to keep existing content')

if st.button('Update Feedback', type='primary', use_container_width=True):
    payload = {'Status': new_status}
    if new_content:
        payload['Content'] = new_content

    update_response = requests.put(
        f'http://web-api:4000/admins/feedback/{int(feedback_id)}',
        json=payload
    )

    if update_response.status_code == 200:
        st.success(f'Feedback {int(feedback_id)} updated.')
    elif update_response.status_code == 404:
        st.error('Feedback not found.')
    else:
        st.error(f'Error {update_response.status_code}: {update_response.text}')


#del feedback
st.write('##### Delete Feedback')

delete_id = st.number_input('Feedback ID to Delete', min_value=1, step=1, value=1)

if st.button('Delete Feedback', type='primary', use_container_width=True):
    delete_response = requests.delete(
        f'http://web-api:4000/admins/feedback/{int(delete_id)}'
    )

    if delete_response.status_code == 200:
        st.success(f'Feedback {int(delete_id)} deleted.')
    elif delete_response.status_code == 404:
        st.error('Feedback not found.')
    else:
        st.error(f'Error {delete_response.status_code}: {delete_response.text}')

st.divider()

#sort by cuisine pref to see what students like at each dining hall
st.write('### Student Cuisine Preferences by Dining Hall')

pref_hall_id = st.number_input('Dining Hall ID', min_value=1, step=1, value=1, key='pref_hall')

if st.button('View Preferences', type='primary', use_container_width=True):
    pref_response = requests.get(
        f'http://web-api:4000/dininghalls/{int(pref_hall_id)}/studentfeedback'
    )

    if pref_response.status_code == 200:
        prefs = pref_response.json()
        if prefs:
            pref_df = pd.DataFrame(prefs)
            st.dataframe(pref_df, use_container_width=True)

            if 'Responses' in pref_df.columns and 'CuisinePref' in pref_df.columns:
                st.write('#### Cuisine Preference Breakdown')
                st.bar_chart(pref_df.set_index('CuisinePref')['Responses'])
        else:
            st.info('No preference data found for this hall.')
    else:
        st.error(f'Error {pref_response.status_code}: {pref_response.text}')