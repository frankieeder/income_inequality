import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data import IRSIncomeByCounty
from data import IRSIncomeByZip
from data import IRSIncome
from data import DQYDJIncomeByAge
from data import PayscaleCeoCompensation
from . import data as streamlit_data
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

STATE_COLS = ['STATEFIPS', 'STATE', 'state_name']
COUNTY_COLS = ['county', 'county_name']

PX_CHOROPLETH_FORMAT_KWARGS = dict(
    marker_line_color='black',
    marker_line_width=0.1,
)


def county_map():
    st.write('# Metrics by County')
    st.write('Select the metric below to visualize per-county.')
    st.write('Data from the '
             '[IRS](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-zip-code-data-soi)')

    county_sums = streamlit_data.get_irs_income_by_county()
    county_boundaries = streamlit_data.get_county_geo_json()
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
    fig.update_traces(**PX_CHOROPLETH_FORMAT_KWARGS)
    st.plotly_chart(fig, use_container_width=True)


def zip_info():
    st.write('# Metrics by Zip')
    st.write('Select the zip to visualize income distribution for.')
    st.write('Data from the '
             '[IRS](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-zip-code-data-soi)')

    income_df = streamlit_data.get_irs_income()
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
    st.write('# Metrics by County')
    st.write('Select a state then county to analyze for .')
    st.write('Data from the '
             '[IRS](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-zip-code-data-soi)')

    #zip_to_fips = get_raw_zip_to_fips()
    fips_county_info = streamlit_data.get_fips_county_info()
    st.write(fips_county_info)
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

    county_sums = streamlit_data.get_irs_income_by_zip()
    zip_boundaries = streamlit_data.get_zip_geo_json(f'ahhhh_{state}')

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
    fig.update_traces(**PX_CHOROPLETH_FORMAT_KWARGS)
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


def plot_total_histogram(income_df):
    by_state = income_df.groupby(STATE_COLS + AGI_STUB_COLS).sum()
    by_state = by_state.reset_index()
    by_state = IRSIncome.calculate_additional_income_stats(by_state)
    st.write("# United States")
    # st.write(by_state)
    st.plotly_chart(plot_income_distribution(by_state), use_container_width=True)


def plot_state_choropleth(income_df):
    state_boundaries = streamlit_data.get_state_geo_json()
    state_df_for_map = income_df.groupby(STATE_COLS).sum().reset_index()
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
    fig.update_traces(**PX_CHOROPLETH_FORMAT_KWARGS)
    st.plotly_chart(fig, use_container_width=True)


def plot_state_histogram(income_df, state):
    this_state_df = income_df.loc[income_df['state_name'] == state]
    state_id = this_state_df['STATEFIPS'].values[0]
    state_postal = this_state_df['STATE'].values[0]

    st.write(f"# {state}")
    st.plotly_chart(plot_income_distribution(this_state_df), use_container_width=True)

    return state_id, state_postal, this_state_df


def plot_county_choropleth(this_state_df, state_id):
    county_boundaries = dict(streamlit_data.get_county_geo_json())
    county_features = [c for c in county_boundaries['features'] if int(c['properties']['STATE']) == state_id]
    county_boundaries_filtered = dict(type='FeatureCollection', features=county_features)
    county_df_for_map = this_state_df.groupby(COUNTY_COLS).sum().reset_index()
    county_df_for_map = IRSIncome.calculate_additional_income_stats(county_df_for_map)
    county_df_for_map['count_name_truc'] = county_df_for_map['county_name'].str.replace(' County', '', regex=False)
    #st.write(county_df_for_map)
    fig = px.choropleth(
        county_df_for_map,
        geojson=county_boundaries_filtered,
        locations='count_name_truc',
        color='mean_income_per_return',
        color_continuous_scale="Viridis",
        featureidkey='properties.NAME',
        # range_color=(0, 12),
        # scope="usa",
        # labels={metric: IRSIncomeByZip.METRIC_NAMES[metric]},
        height=500
    )
    fig.update_traces(**PX_CHOROPLETH_FORMAT_KWARGS)
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)


def plot_county_histogram(this_state_df, county):
    this_county_df = this_state_df.loc[this_state_df['county_name'] == county]
    st.write(f"# {county}")
    st.plotly_chart(plot_income_distribution(this_county_df), use_container_width=True)
    return this_county_df


def plot_zip_code_choropleth(this_county_df, state, state_postal):
    zip_boundaries = dict(streamlit_data.get_zip_geo_json(f"{state_postal.lower()}_{state.lower()}"))
    zip_df_for_map = this_county_df.groupby('zipcode').sum().reset_index()
    zip_df_for_map = IRSIncome.calculate_additional_income_stats(zip_df_for_map)
    #st.write("zip_df_for_map")
    #st.write(zip_df_for_map)
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
    fig.update_traces(**PX_CHOROPLETH_FORMAT_KWARGS)
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)


def plot_zip_code_histogram(this_county_df, zip_code):
    this_zip_code_df = this_county_df.loc[this_county_df['zipcode'] == zip_code]
    st.write(f"# {zip_code}")
    # st.write(this_zip_code_df)
    st.plotly_chart(plot_income_distribution(this_zip_code_df), use_container_width=True)


def deep_dive_zip(this_county_df, zip_code):
    plot_zip_code_histogram(this_county_df, zip_code)


def deep_dive_county(this_state_df, county, state, state_postal):
    this_county_df = plot_county_histogram(this_state_df, county)
    plot_zip_code_choropleth(this_county_df, state, state_postal)

    zip_code = st.selectbox(
        label="County",
        options=list(this_county_df['zipcode'].unique()) + ["All"],
        # TODO: This needs to be updated to include ALL since county and zip boundaries don't align
    )
    if zip_code != "All":
        deep_dive_zip(this_county_df, zip_code)


def deep_dive_state(income_df, state):
    state_id, state_postal, this_state_df = plot_state_histogram(income_df, state)
    plot_county_choropleth(this_state_df, state_id)

    county = st.selectbox(
        label="County",
        options=["All"] + list(this_state_df['county_name'].unique()),
    )
    if county != "All":
        deep_dive_county(this_state_df, county, state, state_postal)


def deep_dive():
    st.write('# Deep Dive')
    st.write('Select a geography to analyze further to start, then repeat. NOTE: in-progress')
    st.write('Data from the '
             '[IRS](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-zip-code-data-soi)')
    income_df = streamlit_data.get_irs_income()

    plot_total_histogram(income_df)
    plot_state_choropleth(income_df)
    state = st.selectbox(
        label="State",
        options=["All"] + list(income_df['state_name'].unique()),
    )
    if state != "All":
        deep_dive_state(income_df, state)


def income_by_age():
    st.write('# Income Distribution by Age')
    st.write('Shows individual gross income distribution by age.')
    st.write(f'Data from [DQYDJ]({DQYDJIncomeByAge.URL})')
    df = streamlit_data.get_dqydj_income_by_age()
    fig = go.Figure()
    for i, c in enumerate(df.columns):
        if c != 'Average':
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[c],
                mode='lines',
                name=c,
                line=dict(color=px.colors.sequential.ice_r[i + 2], width=0.5),
                fill='tonexty' if i > 0 else None,
            ))
        else:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[c],
                mode='lines',
                name=c,
                line=dict(color='white', width=1),
            ))

    st.plotly_chart(fig, use_container_width=True)


def ceo_compensation_ratio():
    st.write('# CEO Compensation Time Ratio')
    st.write('Shows CEO Compensation compared to median worker and your compensation, from the lens of time.')
    st.write(f'Data from [Payscale]({PayscaleCeoCompensation.URL})')
    df = streamlit_data.get_payscale_ceo_compensation()

    st.write('---')

    workday_in_minutes = 60 * 8
    max_ratio = df['ratio'].max()
    max_ratio_info = df[df['ratio'] == max_ratio].to_dict('records')[0]
    st.write(f'If employees of **{max_ratio_info["Company Name"]}** were compensated at the rate of the highest paid '
             f'CEO (**{locale.currency(max_ratio_info["ceo_compensation"], grouping=True)}**), '
             f'the median worker would only need to work')
    st.write(f'## {(workday_in_minutes / max_ratio):2f} minutes per workday')
    st.write('to maintain their overall pay.')

    st.write('---')

    my_pay = st.text_input("My yearly pay, in USD")
    if my_pay:
        my_pay = float(my_pay)
        max_ceo_pay = df['ceo_compensation'].max()
        max_ceo_pay_info = df[df['ceo_compensation'] == max_ceo_pay].to_dict('records')[0]
        my_ratio = max_ceo_pay / my_pay
        st.write(
            f'If you  were compensated at the rate of the highest paid '
            f'CEO (**{max_ceo_pay_info["Company Name"]}, {locale.currency(max_ceo_pay_info["ceo_compensation"], grouping=True)}**), '
            f'you would only need to work')
        st.write(f'## {(workday_in_minutes / my_ratio):2f} minutes per workday')
        st.write('to maintain your overall pay.')
    st.write(df)
