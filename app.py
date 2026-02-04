import streamlit as st
import pandas as pd
from job_engine import fetch_jobs

st.set_page_config(page_title="AI Job Assistant", layout="wide")

st.title("🎯 AI Job Assistant")
st.write("Latest internship opportunities (India)")

with st.spinner("Fetching latest jobs..."):
    df = fetch_jobs()

if df.empty:
    st.warning("No recent jobs found.")
else:
    st.dataframe(df, width="stretch")

    st.download_button(
        label="📥 Download as Excel",
        data=df.to_excel(index=False),
        file_name="jobs.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
