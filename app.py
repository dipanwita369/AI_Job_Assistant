import streamlit as st
from job_engine import fetch_jobs
import io

st.set_page_config(page_title="AI Job Assistant", layout="wide")
st.title("AI Job Assistant 🚀")

if st.button("Fetch Latest Internships"):
    with st.spinner("Fetching jobs..."):
        df = fetch_jobs()

        st.subheader("Latest Opportunities")
        st.dataframe(df, use_container_width=True)

        # Excel download
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)

        st.download_button(
            label="⬇️ Download as Excel",
            data=buffer,
            file_name="ai_job_assistant_jobs.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
