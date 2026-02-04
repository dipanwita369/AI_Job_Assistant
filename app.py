import streamlit as st
from job_engine import fetch_jobs

st.set_page_config(page_title="AI Job Assistant", layout="wide")

st.title("AI Job Assistant")

with st.spinner("Fetching jobs..."):
    df = fetch_jobs()

st.dataframe(df, width="stretch")
