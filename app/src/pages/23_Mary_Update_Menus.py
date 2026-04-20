import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

BASE_URL = 'http://web-api:4000'

st.title('Menus')

# ── Load dining halls for all tabs ───────────────────────────────────────────
try:
    halls    = requests.get(f'{BASE_URL}/dininghalls').json()
    hall_map = {h['Name']: h['HallId'] for h in halls}
except:
    hall_map = {}
    st.error("Couldn't load dining halls.")
    st.stop()

tab1, tab2 = st.tabs(['Update Menu Item', 'Create Menu Item'])


# Tab 1 — PUT /dininghalls/menuitems/{menu_item_id}
with tab1:
    st.write('#### Update an Existing Menu Item')

    selected_hall    = st.selectbox('Select a dining hall', list(hall_map.keys()), key='t1_hall')
    selected_hall_id = hall_map[selected_hall]

    # Load menu items for this hall
    try:
        menu = requests.get(f'{BASE_URL}/dininghalls/{selected_hall_id}/menuitems').json()
    except:
        menu = []
        st.error("Couldn't load menu items.")

    if not menu:
        st.info('No menu items found for this hall.')
    else:
        st.dataframe(pd.DataFrame(menu), use_container_width=True)
        st.divider()

        item_map       = {f"ID {item['ItemId']} — {item['ItemName']}": item for item in menu}
        selected_label = st.selectbox('Select a menu item to update', list(item_map.keys()), key='t1_item')
        selected_item  = item_map[selected_label]

        col1, col2 = st.columns(2)

        with col1:
            new_name = st.text_input('Item name', value=selected_item.get('ItemName', ''), key=f"t1_name_{selected_item['ItemId']}")
            new_desc = st.text_area('Description', value=selected_item.get('Description') or '', key=f"t1_desc_{selected_item['ItemId']}")

        with col2:
            categories  = ['Breakfast', 'Lunch', 'Dinner', 'Snack', 'Dessert', 'Other']
            current_cat = selected_item.get('Category', 'Lunch')
            new_cat     = st.selectbox(
                'Category', categories,
                index=categories.index(current_cat) if current_cat in categories else 0,
                key=f"t1_cat_{selected_item['ItemId']}"
            )
            new_avail = st.checkbox('Currently available', value=bool(selected_item.get('IsAvailable', True)), key=f"t1_avail_{selected_item['ItemId']}")

        if st.button('Update Menu Item', type='primary', use_container_width=True, key='t1_submit'):
            payload = {
                'ItemName':    new_name,
                'Description': new_desc,
                'Category':    new_cat,
                'IsAvailable': new_avail,
                'HallId':      selected_hall_id,
            }
            try:
                resp = requests.put(
                    f"{BASE_URL}/dininghalls/menuitems/{selected_item['ItemId']}",
                    json=payload
                )
                if resp.status_code == 200:
                    st.success(f"✅ '{new_name}' updated successfully!")
                    st.rerun()
                else:
                    st.error(f"Update failed: {resp.json().get('error')}")
            except Exception as e:
                st.error(f'Error: {e}')


# Tab 2 — POST /dininghalls/{hall_id}/menuitems
with tab2:
    st.write('#### Add a New Menu Item')

    selected_hall2    = st.selectbox('Select a dining hall', list(hall_map.keys()), key='t2_hall')
    selected_hall_id2 = hall_map[selected_hall2]

    col1, col2 = st.columns(2)

    with col1:
        item_name = st.text_input('Item name', key='t2_name')
        item_desc = st.text_area('Description (optional)', key='t2_desc')

    with col2:
        item_cat   = st.selectbox('Category',
                                   ['Breakfast', 'Lunch', 'Dinner', 'Snack', 'Dessert', 'Other'],
                                   key='t2_cat')
        item_avail = st.checkbox('Currently available', value=True, key='t2_avail')

    if st.button('Create Menu Item', type='primary', use_container_width=True, key='t2_submit'):
        if not item_name.strip():
            st.warning('Item name is required.')
        else:
            payload = {
                'ItemName':    item_name,
                'Description': item_desc if item_desc else None,
                'Category':    item_cat,
                'IsAvailable': item_avail,
            }
            try:
                resp = requests.post(
                    f"{BASE_URL}/dininghalls/{selected_hall_id2}/menuitems",
                    json=payload
                )
                if resp.status_code == 201:
                    st.success(f"✅ '{item_name}' added to the menu!")
                else:
                    st.error(f"Failed: {resp.json().get('error')}")
            except Exception as e:
                st.error(f'Error: {e}')