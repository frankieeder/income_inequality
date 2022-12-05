import streamlit as st
import plotly.express as px
from data import CountyGeoJSON
from data import IRSIncomeByCounty


@st.cache
def get_irs_income_by_county():
    return IRSIncomeByCounty().process()


@st.cache
def get_county_geo_json():
    return CountyGeoJSON().process()


def county_map():

    county_sums = get_irs_income_by_county()
    county_boundaries = get_county_geo_json()
    metric = st.selectbox(
        label="Metric",
        options=list(IRSIncomeByCounty.METRIC_NAMES.keys()),
        format_func=lambda o: IRSIncomeByCounty.METRIC_NAMES[o],
    )
    fig = px.choropleth(
        county_sums,
        geojson=county_boundaries,
        locations=county_sums.index,
        color=metric,
        color_continuous_scale="Viridis",
        featureidkey='id',
        # range_color=(0, 12),
        scope="usa",
        labels={metric: IRSIncomeByCounty.METRIC_NAMES[metric]},
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)


st.set_page_config(page_title="By County", page_icon="📈", layout='wide')

page_names_to_funcs = {
    "County Map": county_map,
    #"Page 2": page2,
    #"Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
