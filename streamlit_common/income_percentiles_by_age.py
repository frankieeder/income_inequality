import streamlit as st
import plotly.graph_objs as go
import plotly.express as px

from . import data as streamlit_data


def view():
    st.write('# Income Percentiles by Age')
    st.write('Shows individual gross income distribution by age.')
    st.write('Data from [DQYDJ](https://dqydj.com/income-percentile-by-age-calculator/)')
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


def smooth_matrix_along_rows_lowess(mat, *args, **kwargs):
    smoothed = np.empty_like(mat)
    for i, row in enumerate(mat):
        smoothed[i] = statsmodels.nonparametric.smoothers_lowess.lowess(
            endog=row,
            exog=np.arange(len(row)),
            return_sorted=False,
            *args,
            **kwargs,
        )
    return smoothed