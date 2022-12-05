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


def county_plot():
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
        labels={metric: IRSIncomeByCounty.METRIC_NAMES[metric]}
    )
    st.plotly_chart(fig)


if __name__ == '__main__':
    county_plot()
