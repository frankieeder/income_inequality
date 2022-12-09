import streamlit as st
import plotly.express as px
from data import StateGeoJSON
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
def get_state_geo_json():
    return StateGeoJSON().process()


#@st.cache
def get_county_geo_json():
    return CountyGeoJSON().process()


@st.cache
def get_zip_geo_json(state_identifier_string='ca_california', downsample=100):
    zip_geojson = ZipGeoJSON().source(state_identifier_string)
    #st.write(zip_geojson)
    for c in zip_geojson['features']:
        c['geometry']['coordinates'] = c['geometry']['coordinates'][::downsample]
    return zip_geojson


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


AGI_STUB_COLS = ['agi_stub', 'agi_stub_lower_bound', 'agi_stub_desc']


def plot_income_distribution(df, **kwargs):
    df_by_agi_stub = df.groupby(AGI_STUB_COLS).sum()
    df_by_agi_stub = df_by_agi_stub.reset_index()
    df_by_agi_stub = IRSIncome.calculate_additional_income_stats(df_by_agi_stub)
    fig = px.bar(
        df_by_agi_stub,
        x='agi_stub_desc',
        y='N1',
        hover_data={
            'mean_income_per_return': True,
            'mean_income_per_individual': True,
        },
        **kwargs,
    )
    return fig


def deep_dive():
    income_df = get_irs_income()
    STATE_COLS = ['STATEFIPS', 'STATE', 'state_name']
    by_state = income_df.groupby(STATE_COLS + AGI_STUB_COLS).sum()
    by_state = by_state.reset_index()
    by_state = IRSIncome.calculate_additional_income_stats(by_state)
    st.write("# United States")
    #st.write(by_state)
    st.plotly_chart(plot_income_distribution(by_state), use_container_width=True)

    state_boundaries = get_state_geo_json()
    state_df_for_map = by_state.groupby(STATE_COLS).sum().reset_index()
    state_df_for_map = IRSIncome.calculate_additional_income_stats(state_df_for_map)
    fig = px.choropleth(
        state_df_for_map,
        geojson=state_boundaries,
        locations='state_name',
        color='mean_income_per_return',
        color_continuous_scale="Viridis",
        featureidkey='properties.NAME',
        # range_color=(0, 12),
        scope="usa",
        # labels={metric: IRSIncomeByZip.METRIC_NAMES[metric]},
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    state = st.selectbox(
        label="State",
        options=list(by_state['state_name'].unique()) + ["All"],
    )
    if state == "All":
        raise NotImplementedError
    else:
        this_state_df = income_df.loc[income_df['state_name'] == state]
        st.write(this_state_df)
        state_id = this_state_df['STATEFIPS'].values[0]
        state_postal = this_state_df['STATE'].values[0]
        st.write(state_id)
        st.write(f"# {state}")
        #st.write(this_state_df)
        st.plotly_chart(plot_income_distribution(this_state_df), use_container_width=True)

    COUNTY_COLS = ['county', 'county_name']
    county_boundaries = dict(get_county_geo_json())
    county_features = [c for c in county_boundaries['features'] if int(c['properties']['STATE']) == state_id]
    county_boundaries_filtered = dict(type='FeatureCollection', features=county_features)
    #st.write(county_boundaries_filtered)
    #st.write(county_boundaries)
    county_df_for_map = this_state_df.groupby(COUNTY_COLS).sum().reset_index()
    county_df_for_map = IRSIncome.calculate_additional_income_stats(county_df_for_map)
    county_df_for_map['count_name_truc'] = county_df_for_map['county_name'].str.replace(' County', '', regex=False)
    st.write(county_df_for_map)
    fig = px.choropleth(
        county_df_for_map,
        geojson=county_boundaries_filtered,
        locations='count_name_truc',
        color='mean_income_per_return',
        color_continuous_scale="Viridis",
        featureidkey='properties.NAME',
        # range_color=(0, 12),
        #scope="usa",
        # labels={metric: IRSIncomeByZip.METRIC_NAMES[metric]},
        height=500
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

    county = st.selectbox(
        label="County",
        options=list(this_state_df['county_name'].unique()) + ["All"],
    )
    if county == "All":
        raise NotImplementedError
    else:
        this_county_df = this_state_df.loc[this_state_df['county_name'] == county]
        st.write(f"# {county}")
        #st.write(this_county_df)
        st.plotly_chart(plot_income_distribution(this_county_df), use_container_width=True)

    zip_boundaries = dict(get_zip_geo_json(f"{state_postal.lower()}_{state.lower()}"))
    # county_features = [c for c in county_boundaries['features'] if int(c['properties']['STATE']) == state_id]
    # county_boundaries_filtered = dict(type='FeatureCollection', features=county_features)
    # st.write(county_boundaries_filtered)
    # st.write(county_boundaries)
    #st.write(zip_boundaries)
    zip_df_for_map = this_county_df.groupby('zipcode').sum().reset_index()
    zip_df_for_map = IRSIncome.calculate_additional_income_stats(zip_df_for_map)
    st.write("zip_df_for_map")
    st.write(zip_df_for_map)
    fig = px.choropleth(
        zip_df_for_map,
        geojson=zip_boundaries,
        locations='zipcode',
        color='mean_income_per_return',
        color_continuous_scale="Viridis",
        featureidkey='properties.ZCTA5CE10',
        # range_color=(0, 12),
        # scope="usa",
        # labels={metric: IRSIncomeByZip.METRIC_NAMES[metric]},
        height=500
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

    zip_code = st.selectbox(
        label="County",
        options=list(this_county_df['zipcode'].unique()) + ["All"],  # TODO: This needs to be updated to include ALL since county and zip boundaries don't align
    )
    if zip_code == "All":
        raise NotImplementedError
    else:
        this_zip_code_df = this_county_df.loc[this_county_df['zipcode'] == zip_code]
        st.write(f"# {zip_code}")
        #st.write(this_zip_code_df)
        st.plotly_chart(plot_income_distribution(this_zip_code_df), use_container_width=True)


if __name__ == "__main__":
    deep_dive()
