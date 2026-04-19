import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')

SideBarLinks()

BASE_URL = 'http://localhost:4000'

st.title('Dining Hall Usage & Reports')

# getting usage stats data and converting it into a dataframe
try:
    stats_res = requests.get(f'{BASE_URL}/admins/usagestats')
    if stats_res.status_code == 200:
        stats = pd.DataFrame(stats_res.json())
    else:
        stats = pd.DataFrame()
        
except:
    stats = pd.DataFrame()
    st.warning("Usage Stats not loading. Something went wrong.")


# visitor count chart
if not stats.empty:
    stats['VisitorCount'] = pd.to_numeric(stats['VisitorCount'])


    # stats overview
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Total Visitors',  f"{int(stats['VisitorCount'].sum()):,}")
    c2.metric('Avg per Session', f"{stats['VisitorCount'].mean():.0f}")
    c3.metric('Busiest Hall',    stats.groupby('HallName')['VisitorCount'].sum().idxmax())
    c4.metric('Busiest Day',     stats.groupby('DayOfWeek')['VisitorCount'].sum().idxmax())

    st.divider()

    # dining hall visitor stats
    st.write('### Where are students eating?')
    hall_totals = stats.groupby('HallName')['VisitorCount'].sum().sort_values()
    st.bar_chart(hall_totals)

    col1, col2 = st.columns(2)

    with col1:
        st.write('### Busiest days of the week')
        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        day_totals = stats.groupby('DayOfWeek')['VisitorCount'].sum()
        st.bar_chart(day_totals)

    with col2:
        st.write('### Average visitors per hall')
        hall_avg = stats.groupby('HallName')['VisitorCount'].mean().round(0).sort_values(ascending=False)
        st.bar_chart(hall_avg)

    st.divider()

    # all visitor data 
    st.write('### Raw data')
    st.write('All the visitor records we have on file:')
    st.dataframe(stats[['HallName','DayOfWeek','VisitorCount','PeakHour','TimeStamp']], )

    # download data 
    st.download_button(
        'Download visitor data as CSV',
        data=stats.to_csv(index=False).encode('utf-8'),
        file_name='visitor_stats.csv',
        mime='text/csv',
    )

st.divider()

# section for reports 
st.write('### Reports')
st.write('Create, view, update, or delete reports below.')

# load reports
try:
    reports_res = requests.get(f'{BASE_URL}/admins/reports')
    reports = pd.DataFrame(reports_res.json()) if reports_res.status_code == 200 else pd.DataFrame()
except:
    reports = pd.DataFrame()
    st.warning("Couldn't load reports.")

if not reports.empty:
    st.dataframe(reports[['ReportId','Title','Format','StartDate','EndDate']], use_container_width=True)
    st.download_button(
        'Download reports as CSV',
        data=reports.to_csv(index=False).encode('utf-8'),
        file_name='reports.csv',
        mime='text/csv',
    )
else:
    st.info('No reports yet — create one below!')

st.divider()

tab_create, tab_update, tab_delete = st.tabs(['+ Create', ' Update', ' Delete'])

# creating new report 
with tab_create:
    st.write('Fill in the details to create a new report.')
    report_id = st.number_input('Report ID',  min_value=1, step=1, key='c_id')
    title  = st.text_input('Title',placeholder='e.g. Weekly Visitor Report', key='c_title')
    fmt = st.selectbox('Format', ['PDF', 'Excel', 'CSV'], key='c_fmt')
    c1, c2 = st.columns(2)
    start = c1.date_input('Start Date',key='c_start')
    end = c2.date_input('End Date',key='c_end')

    if st.button('Create report', type='primary', key='create_btn'):
        if not title.strip():
            st.warning('Report needs a title')
        else:
            payload = {
                'ReportId': int(report_id),
                'Title': title.strip(),
                'Format': fmt,
                'StartDate': str(start),
                'EndDate': str(end),
            }
            r = requests.post(f'{BASE_URL}/admins/reports', json=payload)
            if r.status_code == 201:
                st.success('Report created! Re-sign in to see it.')
            else:
                st.error(f'Something went wrong: {r.json().get("error", r.status_code)}')

# updating new report
with tab_update:
    st.write('Change the title or format of an existing report.')
    upd_id    = st.number_input('Report ID to update', min_value=1, step=1, key='u_id')
    upd_title = st.text_input('New title (leave blank to keep current)', key='u_title')
    upd_fmt   = st.selectbox('New format', ['PDF', 'Excel', 'CSV'], key='u_fmt')

    if st.button('Update report', type='primary', key='update_btn'):
        payload = {'Format': upd_fmt}
        if upd_title.strip():
            payload['Title'] = upd_title.strip()
        r = requests.put(f'{BASE_URL}/admins/reports/{upd_id}', json=payload)
        if r.status_code == 200:
            st.success('Report updated!')
        elif r.status_code == 404:
            st.error("Couldn't find a report with that ID.")
        else:
            st.error(f'Something went wrong: {r.json().get("error", r.status_code)}')

# delete 
with tab_delete:
    st.write('Permanently remove a report by its ID.')
    st.warning('This cannot be undone.')
    del_id = st.number_input('Report ID to delete', min_value=1, step=1, key='d_id')

    if st.button('Delete report', type='primary', key='delete_btn'):
        r = requests.delete(f'{BASE_URL}/admins/reports/{del_id}')
        if r.status_code == 200:
            st.success(f'Report {del_id} deleted.')
            
        elif r.status_code == 404:
            st.error("Couldn't find a report with that ID.")
            
        else:
            st.error(f'Something went wrong: {r.json().get("error", r.status_code)}')