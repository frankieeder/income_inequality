import streamlit as st

from streamlit_common import zip_info
from streamlit_common import county_map
from streamlit_common import zip_map
from streamlit_common import deep_dive
from streamlit_common import income_by_age

st.set_page_config(page_title="Income by Geo - US IRS", page_icon="📈", layout='wide')

page_names_to_funcs = {
    "Income by Age": income_by_age,
    "Deep Dive": deep_dive,
    # "County Map": county_map,
    # "Zip Code Info": zip_info,
    # "Zip Map": zip_map,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
