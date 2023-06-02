import streamlit as st

from streamlit_common import views

st.set_page_config(page_title="Income by Geo - US IRS", page_icon="📈", layout='wide')

page_names_to_funcs = {
    "CEO Compensation Ratio": views.ceo_compensation_ratio,
    "Metrics mapped by County": views.county_map,
    # "Metrics mapped by Zip in County": views.zip_map,
    "Metrics by Zip": views.zip_info,
    "Income by Age": views.income_by_age,
    "BETA - Geographic Deep Dive": views.deep_dive,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
