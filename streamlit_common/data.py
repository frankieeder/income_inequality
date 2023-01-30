import streamlit as st
from data import StateGeoJSON
from data import CountyGeoJSON
from data import ZipGeoJSON
from data import IRSIncomeByCounty
from data import IRSIncomeByZip
from data import IRSIncome
from data import ZipToFips
from data import FipsCountyInfo
from data import DQYDJIncomeByAge


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
def get_state_geo_json():
    return StateGeoJSON().process()


#@st.cache
def get_county_geo_json():
    return CountyGeoJSON().process()


# @st.experimental_singleton
def get_dqydj_income_by_age():
    return DQYDJIncomeByAge().process()


@st.cache
def get_zip_geo_json(state_identifier_string, downsample=100):
    zip_geojson = ZipGeoJSON().source(state_identifier_string)
    for c in zip_geojson['features']:
        c['geometry']['coordinates'] = c['geometry']['coordinates'][::downsample]
    return zip_geojson