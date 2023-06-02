import streamlit as st
import numpy as np
import statsmodels.api as sm

import plotly.graph_objs as go
import plotly.express as px

from data.income_percentiles_by_age.dqydj_income_by_age import DQYDJIncomeByAge


@st.cache_resource
def get_dqydj_income_by_age():
    return DQYDJIncomeByAge().process()


def view():
    st.write("# Income Percentiles by Age")
    st.write("Shows individual gross income distribution by age.")
    st.write(
        "Data from [DQYDJ](https://dqydj.com/income-percentile-by-age-calculator/)"
    )
    df = get_dqydj_income_by_age()

    st.markdown('## Income Surface')
    z_values = df.values
    smooth = st.checkbox(
        "Smooth surface",
        value=True,
        help="Apples trend line smoothing (LOWESS) across each percentile to filter noisy portions of dataset",
    )
    if smooth:
        z_values = smooth_matrix_along_rows_lowess(z_values)
    top_left, top_right = st.columns(2)
    with top_left:
        st.plotly_chart(generate_surface_figure(z_values), use_container_width=True)
    with top_right:
        st.plotly_chart(generate_contour_figure(z_values), use_container_width=True)

    st.markdown("## Isolate Age(s) & Percentile(s)")

    bottom_left, bottom_right = st.columns(2)
    with bottom_left:
        ages = st.multiselect(
            label="Age",
            options=df.columns,
            default=['20', '30', '40', '50', '60', '70'],
        )
        st.plotly_chart(generate_age_plot(df, ages), use_container_width=True)
    with bottom_right:
        percentiles = st.multiselect(
            label="Percentile",
            options=df.index,
            default=[0.1, 0.5, 0.75, 0.9, 0.99],
        )
        st.plotly_chart(generate_percentile_plot(df.T, percentiles), use_container_width=True)


def generate_age_plot(df, ages):
    data = []
    for i, age in enumerate(ages):
        fig = px.line(
            df[age],
        )
        fig.update_traces(line_color=px.colors.sequential.ice_r[i])
        data += fig.data
    full_fig = go.Figure(data)
    full_fig.update_layout(
        legend_title_text='Age',
        title_text='Income Percentiles Across Ages',
        xaxis_title_text='Percentile',
        yaxis_title_text='Income',
    )
    return full_fig


def generate_percentile_plot(df, percentiles):
    data = []
    for i, percentile in enumerate(percentiles):
        fig = px.scatter(
            df[percentile],
            trendline='lowess',
        )
        fig.update_traces(line_color=px.colors.sequential.ice_r[i])
        data += fig.data
    full_fig = go.Figure(data)
    full_fig.update_layout(
        legend_title_text='Percentile',
        title_text='Income/Age Curve Across Percentiles',
        xaxis_title_text='Age',
        yaxis_title_text='Income',
    )
    return full_fig


def add_common_figure_formatting(fig: go.Figure) -> go.Figure:
    fig.update_traces(
        hovertemplate="""Age: %{x}<br>Percentile %{y}<br>Income: %{z}""",
    )
    return fig


def generate_surface_figure(z_values) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Surface(
                z=z_values,
                colorscale="ice_r",
                #             contours = {
                #                 #"y": {"show": True, "size": 0.01, "color":"black"},
                #                 #"z": {"show": True, "start": 0.5, "end": 0.8, "size": 0.01}
                #             }
            )
        ]
    )
    fig.update_layout(
        title="Income by Income Percentile and Age - Surface",
        scene=dict(
            xaxis_title="Age", yaxis_title="Percentile", zaxis_title="Income (USD)"
        ),
    )
    fig = add_common_figure_formatting(fig)
    return fig


def generate_contour_figure(z_values) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Contour(
                z=z_values,
                colorscale="ice_r",
                contours=dict(
                    showlabels=True,  # show labels on contours
                    labelfont=dict(  # label font properties
                        size=8,
                        color="white",
                    ),
                ),
            )
        ]
    )
    fig.update_layout(
        title="Income by Income Percentile and Age - Contour Plot",
        xaxis_title="Age",
        yaxis_title="Percentile",
    )
    fig = add_common_figure_formatting(fig)
    return fig


def smooth_matrix_along_rows_lowess(mat, *args, **kwargs):
    smoothed = np.empty_like(mat)
    for i, row in enumerate(mat):
        smoothed[i] = sm.nonparametric.lowess(
            endog=row,
            exog=np.arange(len(row)),
            return_sorted=False,
            *args,
            **kwargs,
        )
    return smoothed
