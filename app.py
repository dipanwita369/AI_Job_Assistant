import streamlit as st
import pandas as pd
from job_engine import fetch_jobs

st.set_page_config(page_title="AI Job Assistant", layout="wide")

st.title("🤖 AI Job Assistant – India")
st.write("Fetch latest **Data & Analytics internships** from top companies.")

if st.button("🚀 Fetch Latest Jobs"):
    with st.spinner("Fetching jobs..."):
        df = fetch_jobs()
    st.success("Jobs updated successfully!")

    st.subheader("📊 Latest Job Listings")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="⬇ Download Excel",
        data=df.to_excel(index=False),
        file_name="jobs_final.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    try:
        df = pd.read_excel("jobs_final.xlsx")
        st.subheader("📊 Existing Jobs")
        st.dataframe(df, use_container_width=True)
    except:
        st.info("Click **Fetch Latest Jobs** to load data.")
