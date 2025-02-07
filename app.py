import streamlit as st

st.set_page_config(page_title="Main App", layout="wide")

st.image("richter logo_schwarz.png", width=250)
st.title("Welcome to the SPD Comparison App")
st.write(
    """
    This app allows you to compare Spectral Power Distributions (SPDs) from different files.
    Use the sidebar to navigate to the SPD Comparison Page.
    """
)

