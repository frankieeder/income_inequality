import streamlit as st
import plotly.express as px
from data import CountyGeoJSON
from data import IRSIncomeByCounty
from data import IRSIncomeByZip
from data import IRSIncome


@st.cache
def get_irs_income_by_county():
    return IRSIncomeByCounty().process()


@st.cache
def get_irs_income_by_zip():
    return IRSIncomeByZip().process()


@st.cache
def get_irs_income():
    return IRSIncome().process()


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


def zip_info():
    income_df = get_irs_income()
    #county_boundaries = get_county_geo_json()
    zip_code = st.text_input(
        label="Zip Code",
        value='90210',
        #options=list(income_df['zipcode'].unique()),
        #format_func=lambda o: IRSIncomeByCounty.METRIC_NAMES[o],
    )
    zipcode_data = income_df[income_df['zipcode'] == zip_code]
    if len(zipcode_data):
        fig = px.bar(
            zipcode_data,
            x='agi_stub_desc',
            y='N1'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"Zip code {zip_code} not found")

if __name__ == "__main__":
    zip_info()
    x = 2
