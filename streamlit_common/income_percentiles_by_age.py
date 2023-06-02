import streamlit as st
import numpy as np
import statsmodels.api as sm

import plotly.graph_objs as go
import plotly.express as px

from . import data as streamlit_data


def view():
    st.write('# Income Percentiles by Age')
    st.write('Shows individual gross income distribution by age.')
    st.write('Data from [DQYDJ](https://dqydj.com/income-percentile-by-age-calculator/)')
    df = streamlit_data.get_dqydj_income_by_age()
    z_values = df.values
    smooth = st.checkbox("Smooth raw data", value=True)
    if smooth:
        z_values = smooth_matrix_along_rows_lowess(z_values)

    left, right = st.columns(2)
    with left:
        st.plotly_chart(generate_surface_figure(z_values), use_container_width=True)
    with right:
        st.plotly_chart(generate_contour_figure(z_values), use_container_width=True)


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
                colorscale='ice_r',
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
            xaxis_title="Age",
            yaxis_title="Percentile",
            zaxis_title="Income (USD)"
        )
    )
    fig = add_common_figure_formatting(fig)
    return fig


def generate_contour_figure(z_values) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Contour(
                z=z_values,
                colorscale='ice_r',
                contours=dict(
                    showlabels=True,  # show labels on contours
                    labelfont=dict(  # label font properties
                        size=8,
                        color='white',
                    )
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