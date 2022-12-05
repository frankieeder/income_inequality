import streamlit as st
import plotly.express as px
from data import CountyGeoJSON
from data import ZipGeoJSON
from data import IRSIncomeByCounty
from data import IRSIncomeByZip
from data import IRSIncome
from data import ZipToFips
from data import FipsCountyInfo


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
def get_raw_zip_to_fips():
    return ZipToFips().source()


@st.cache
def get_fips_county_info():
    return FipsCountyInfo().process()


@st.cache
def get_county_geo_json():
    return CountyGeoJSON().process()


@st.cache
def get_zip_geo_json(state_identifier_string='ca_california'):
    return ZipGeoJSON().source(state_identifier_string)


def county_map():
    county_sums = get_irs_income_by_county()
    county_boundaries = get_county_geo_json()
    metric = st.selectbox(
        label="Metric",
        options=list(IRSIncomeByCounty.METRIC_NAMES.keys()),
        format_func=lambda o: IRSIncomeByCounty.METRIC_NAMES[o],
        index=3,
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
        height=500,
        hover_data={
            'county_name': True,
            'state_name': True,
        }
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


def zip_map():
    #zip_to_fips = get_raw_zip_to_fips()
    fips_county_info = get_fips_county_info()
    state_options = fips_county_info['state_name'].unique()
    state = st.selectbox(
        label="State",
        options=state_options,
    )
    #county_options = fips_county_info[fips_county_info['state_name'] == state]

    # county = st.selectbox(
    #     label="Conty",
    #     options=county_options['county_name'].values,
    # )
    #
    # county_code = county_options[county_options['county_name'] == county].index.values[0]
    # zips_in_county = zip_to_fips[zip_to_fips['county'] == county_code]
    # zips_in_county = zips_in_county['zip']
    # zips_in_county = set(zips_in_county.values)

    #st.write(zips_in_county)

    # PLOT

    county_sums = get_irs_income_by_zip()
    zip_boundaries = get_zip_geo_json()

    metric = st.selectbox(
        label="Metric",
        options=list(IRSIncomeByZip.METRIC_NAMES.keys()),
        format_func=lambda o: IRSIncomeByZip.METRIC_NAMES[o],
    )
    fig = px.choropleth(
        county_sums,
        geojson=zip_boundaries,
        locations=county_sums.index,
        color=metric,
        color_continuous_scale="Viridis",
        featureidkey='properties.ZCTA5CE10',
        # range_color=(0, 12),
        scope="usa",
        labels={metric: IRSIncomeByZip.METRIC_NAMES[metric]},
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    zip_map()
