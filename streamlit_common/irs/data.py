import streamlit as st
from data.geography.state_geojson import StateGeoJSON
from data.geography.county_geojson import CountyGeoJSON
from data.geography.zip_geojson import ZipGeoJSON
from data.geography.zip_to_fips import ZipToFips
from data.geography.fips_county_info import FipsCountyInfo
from data.irs.irs_income_by_county import IRSIncomeByCounty
from data.irs.irs_income_by_zip import IRSIncomeByZip
from data.irs.irs_income import IRSIncome


@st.cache_resource
def get_irs_income_by_county():
    return IRSIncomeByCounty().process()


@st.cache_resource
def get_irs_income_by_zip():
    return IRSIncomeByZip().process()


@st.cache_resource
def get_irs_income():
    return IRSIncome().process()


@st.cache_resource
def get_raw_zip_to_fips():
    return ZipToFips().source()


@st.cache_resource
def get_fips_county_info():
    return FipsCountyInfo().process()


@st.cache_resource
def get_state_geo_json():
    return StateGeoJSON().process()


@st.cache_resource
def get_county_geo_json():
    return CountyGeoJSON().process()


@st.cache_resource
def get_zip_geo_json(state_identifier_string, downsample=100):
    zip_geojson = ZipGeoJSON().source(state_identifier_string)
    for c in zip_geojson["features"]:
        c["geometry"]["coordinates"] = c["geometry"]["coordinates"][::downsample]
    return zip_geojson
