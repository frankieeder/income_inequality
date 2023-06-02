import streamlit as st

st.set_page_config(page_title="Income by Geo - US IRS", page_icon="📈", layout='wide')

from streamlit_common import views
from streamlit_common import income_percentiles_by_age

page_names_to_funcs = {
    "Income Percentiles by Age": income_percentiles_by_age.view,
    "Metrics mapped by County": views.county_map,
    # "Metrics mapped by Zip in County": views.zip_map,
    "Metrics by Zip": views.zip_info,
    "BETA - Geographic Deep Dive": views.deep_dive,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
