# job_engine.py
import requests
import pandas as pd
import os
import re
from datetime import datetime, timedelta

API_KEY = os.getenv("SERP_API_KEY")

if not API_KEY:
    raise ValueError("SERP_API_KEY not set")

SEARCH_ROLES = [
    "Data Analyst internship India",
    "Business Analyst internship India",
    "Finance Analyst internship India",
    "Data Scientist internship India",
    "Python Developer Intern",
    "Platform Intern"
]


def parse_posted_date(text):
    if not text:
        return None

    text = text.lower()

    if "today" in text or "just" in text:
        return datetime.today()

    match = re.search(r"(\d+)\s+(day|week|month)", text)
    if not match:
        return None

    value, unit = int(match.group(1)), match.group(2)

    if unit == "day":
        return datetime.today() - timedelta(days=value)
    if unit == "week":
        return datetime.today() - timedelta(weeks=value)
    if unit == "month":
        return datetime.today() - timedelta(days=value * 30)

    return None


def fetch_jobs():
    url = "https://serpapi.com/search.json"
    jobs = []

    for role in SEARCH_ROLES:
        params = {
            "engine": "google_jobs",
            "q": role,
            "hl": "en",
            "api_key": API_KEY
        }

        res = requests.get(url, params=params, timeout=20)
        res.raise_for_status()
        data = res.json()

        for job in data.get("jobs_results", []):
            posted_text = job.get("detected_extensions", {}).get("posted_at", "")
            posted_date = parse_posted_date(posted_text)

            if not posted_date:
                continue

            if (datetime.today() - posted_date).days > 30:
                continue

            jobs.append({
                "Company": job.get("company_name"),
                "Role": job.get("title"),
                "Location": job.get("location"),
                "Posted": posted_text,
                "Posted_Date": posted_date,
                "Apply Link": job.get("apply_options", [{}])[0].get("link")
            })

    df = pd.DataFrame(jobs)

    if df.empty:
        return df

    df.sort_values("Posted_Date", ascending=False, inplace=True)
    df.drop(columns=["Posted_Date"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df
