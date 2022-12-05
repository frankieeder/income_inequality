import streamlit as st

from streamlit_common import zip_info
from streamlit_common import county_map

st.set_page_config(page_title="By County", page_icon="📈", layout='wide')

page_names_to_funcs = {
    "Zip Code Info": zip_info,
    "County Map": county_map,
    #"Page 2": page2,
    #"Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
