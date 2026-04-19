import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

BASE_URL = 'http://web-api:4000'

st.title('Student Feedback')
st.write('Browse and filter feedback submitted by students.')

# Load all dining halls for dropdowns
try:
    halls    = requests.get(f'{BASE_URL}/dininghalls').json()
    hall_map = {h['Name']: h['HallId'] for h in halls}
except:
    hall_map = {}
    st.error("Couldn't load dining halls.")
    st.stop()

tab1, tab2 = st.tabs(['Student Feedback', 'Student Preferences'])


# Tab 1 
with tab1:

    # Filters 
    col1, col2 = st.columns(2)
    status       = col1.selectbox('Filter by status', ['All', 'positive', 'neutral', 'negative'])
    hall_options = ['All'] + list(hall_map.keys())
    selected     = col2.selectbox('Filter by Dining Hall', hall_options)

    params = {}
    if status != 'All':
        params['status'] = status
    if selected != 'All':
        params['hall_id'] = hall_map[selected]

    # GET /admins/feedback 
    try:
        res = requests.get(f'{BASE_URL}/admins/feedback', params=params)
        if res.status_code != 200:
            st.error(f'Error {res.status_code}: {res.json().get("error", "Unknown")}')
            st.stop()
        data = res.json()
    except requests.exceptions.ConnectionError:
        st.error("Couldn't connect to the API.")
        st.stop()

    if not data:
        st.info('No feedback found for those filters.')
        st.stop()

    # Summary metrics 
    positive = sum(1 for f in data if f['Status'] == 'positive')
    neutral  = sum(1 for f in data if f['Status'] == 'neutral')
    negative = sum(1 for f in data if f['Status'] == 'negative')

    m1, m2, m3, m4 = st.columns(4)
    m1.metric('Total',       len(data))
    m2.metric('🟢 Positive', positive)
    m3.metric('🟡 Neutral',  neutral)
    m4.metric('🔴 Negative', negative)

    st.divider()

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.write('#### Update or Delete a Submission')

    fb_ids   = [fb.get('FeedbackSubmissionId') or fb.get('feedbacksubmissionid') or i
                for i, fb in enumerate(data)]
    previews = [f"ID {fb_ids[i]} — {fb.get('Content','')[:60]}..." for i, fb in enumerate(data)]
    id_map   = dict(zip(previews, fb_ids))
    status_map = {fb_ids[i]: (fb.get('Status') or fb.get('status') or 'neutral') for i, fb in enumerate(data)}

    selected_preview = st.selectbox('Select a submission', previews, key='tab1_select')
    selected_fb_id   = id_map[selected_preview]

    col1, col2 = st.columns(2)

    with col1:
        new_status = st.selectbox(
            'New status',
            ['positive', 'neutral', 'negative'],
            index=['positive', 'neutral', 'negative'].index(status_map[selected_fb_id]),
            key='tab1_new_status'
        )
        if st.button('Update status', type='primary', use_container_width=True):
            try:
                resp = requests.put(
                    f"{BASE_URL}/admins/feedback/{selected_fb_id}",
                    json={'Status': new_status}
                )
                if resp.status_code == 200:
                    st.success('✅ Status updated!')
                    st.rerun()
                else:
                    st.error(resp.json().get('error'))
            except Exception as e:
                st.error(f'Error: {e}')

    with col2:
        st.write('')
        st.write('')
        if st.button('🗑️ Delete this submission', use_container_width=True):
            try:
                resp = requests.delete(f"{BASE_URL}/admins/feedback/{selected_fb_id}")
                if resp.status_code == 200:
                    st.success('Deleted.')
                    st.rerun()
                else:
                    st.error(resp.json().get('error'))
            except Exception as e:
                st.error(f'Error: {e}')


# Tab 2 — GET /dininghalls/{id}/studentfeedback
# Cuisine and dietary preference breakdown per hall

with tab2:
    st.write('#### Student Preferences by Dining Hall')
    st.caption('cuisine and dietary trends per dining hall.')

    hall_options2    = list(hall_map.keys())
    selected_hall    = st.selectbox('Select a dining hall', hall_options2, key='tab2_hall')
    selected_hall_id = hall_map[selected_hall]

    # GET /dininghalls/{id}/studentfeedback
    try:
        res2 = requests.get(
            f'{BASE_URL}/dininghalls/{selected_hall_id}/studentfeedback'
        )
        if res2.status_code != 200:
            st.error(f'Error {res2.status_code}: {res2.json().get("error", "Unknown")}')
            st.stop()
        hall_feedback = res2.json()
    except requests.exceptions.ConnectionError:
        st.error("Couldn't connect to the API.")
        st.stop()

    if not hall_feedback:
        st.info(f'No feedback on record for {selected_hall}.')
    else:
        st.write(f"**{len(hall_feedback)} submission(s)** for {selected_hall}")
        st.divider()

        # Aggregate cuisine and dietary counts
        cuisine_counts = {}
        dietary_counts = {}
        for fb in hall_feedback:
            c = fb.get('CuisinePref')
            d = fb.get('DietaryRestriction')
            if c:
                cuisine_counts[c] = cuisine_counts.get(c, 0) + 1
            if d:
                dietary_counts[d] = dietary_counts.get(d, 0) + 1

        col1, col2 = st.columns(2)

        with col1:
            st.write('**Cuisine Preferences**')
            if cuisine_counts:
                df_cuisine = pd.DataFrame(
                    cuisine_counts.items(), columns=['Cuisine', 'Count']
                ).sort_values('Count', ascending=False)
                st.bar_chart(df_cuisine.set_index('Cuisine'))
            else:
                st.info('No cuisine data.')

        with col2:
            st.write('**Dietary Restrictions**')
            if dietary_counts:
                df_dietary = pd.DataFrame(
                    dietary_counts.items(), columns=['Restriction', 'Count']
                ).sort_values('Count', ascending=False)
                st.bar_chart(df_dietary.set_index('Restriction'))
            else:
                st.info('No dietary restriction data.')

        st.divider()
        st.write('**Raw Submissions**')
        st.dataframe(pd.DataFrame(hall_feedback), use_container_width=True)