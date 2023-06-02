import streamlit as st


def write_welcome_header():
    st.write("# Income Inequality")
    st.write(
        "This web app offers a few different lenses into income inequality in the USA."
    )
    st.write(
        "Use the sidebar on the left to explore different data sources and"
        " visualizations, and consider tipping a"
        " [one-time](https://paypal.me/inkfreeread) or"
        " [recurring](https://www.patreon.com/frankieeder) coffee if you found them"
        " useful."
    )
    st.markdown(" --- ")


def preface_with_welcome_header(f):
    def welcome_prefacer():
        write_welcome_header()
        f()

    return welcome_prefacer
