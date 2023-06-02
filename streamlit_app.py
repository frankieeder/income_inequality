import streamlit as st

st.set_page_config(page_title="Income by Geo - US IRS", page_icon="📈", layout="wide")

from streamlit_common.irs import views as irs_views
from streamlit_common import income_percentiles_by_age
from streamlit_common.common import preface_with_welcome_header

page_names_to_funcs = {
    "Income Percentiles by Age": income_percentiles_by_age.view,
    "IRS Metrics mapped by County": irs_views.county_map,
    # "Metrics mapped by Zip in County": views.zip_map,
    "IRS Metrics by Zip": irs_views.zip_info,
    "BETA - IRS Metrics Geographic Deep Dive": irs_views.deep_dive,
}
page_names_to_funcs = {k: preface_with_welcome_header(v) for k, v in page_names_to_funcs.items()}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
