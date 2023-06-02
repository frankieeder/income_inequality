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
        z_values = smooth_matrix_along_rows_lowess

    fig = go.Figure(
        data=[
            go.Surface(
                z=smooth_matrix_along_rows_lowess(df.values),
                colorscale='ice_r',
                #             contours = {
                #                 #"y": {"show": True, "size": 0.01, "color":"black"},
                #                 #"z": {"show": True, "start": 0.5, "end": 0.8, "size": 0.01}
                #             }
            )
        ]
    )
    fig.update_layout(
        title="Income by Income Percentile and Age",
    )
    fig.update_traces(
        hovertemplate="""Age: %{x}<br>Percentile %{y}<br>Income: %{z}""",
    )
    st.plotly_chart(fig, use_container_width=True)


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