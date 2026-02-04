# -----------------------------
# job_engine.py
# Core job fetching + scoring logic
# -----------------------------

import requests
import pandas as pd
import os

# -----------------------------
# Configuration
# -----------------------------

API_KEY = os.getenv("SERP_API_KEY")   # ✅ Secure API key


if not API_KEY:
    raise ValueError(
        "SERP_API_KEY not found. Please set it as an environment variable."
    )

SEARCH_ROLES = [
    "Data Analyst internship India",
    "Business Analyst internship India",
    "Finance Analyst internship India",
    "Data Scientist internship India",
    "Data Engineer internship India"
]

# -----------------------------
# Company Priority Map
# -----------------------------

TOP_COMPANIES = {
    "Google": 100,
    "Amazon": 100,
    "Microsoft": 100,
    "Meta": 100,
    "Apple": 100,
    "Netflix": 100,
    "Databricks": 100,
    "Anthropic": 100,
    "Hugging Face": 100,
    "Salesforce": 100,
    "ServiceNow": 100,
    "Adobe": 100,
    "Atlassian": 100,
    "MongoDB": 100,

    "Goldman Sachs": 100,
    "Capital One": 100,
    "American Express": 100,
    "Mastercard": 100,
    "Visa": 100,
    "Stripe": 100,
    "Square": 100,
    "PayPal": 100,
    "Coinbase": 100,
    "Klarna": 100,
    "Revolut": 100,
    "Wise": 100,

     "PhonePe": 90,
    "Razorpay": 90,
    "Zerodha": 90,
    "Groww": 90,
    "CRED": 90,
    "Paytm": 90,
    "Navi": 90,
    "BharatPe": 90,
    "INDmoney": 90,
    "Upstox": 90,
    "Jupiter": 90,
    "Slice": 90,
    "Fi": 90,
    "Cashfree Payments": 90,
    "Juspay": 90,

    "Flipkart": 90,
    "Myntra": 90,
    "Meesho": 90,
    "Swiggy": 90,
    "Zomato": 90,
    "Blinkit": 90,
    "Zepto": 90,
    "Ola": 90,
    "Dream11": 90,
    "Cure.fit": 90,

     "Walmart": 80,
    "Target": 80,
    "Tesco": 80,
    "SAP Labs": 80,
    "Cisco": 80,
    "Dell": 80,
    "Siemens": 80,
    "Honeywell": 80,
    "Intel": 80,
    "AMD": 80,
    "Arista Networks": 80,
    "Infoblox": 80,
    "Autodesk": 80,
    "Qlik": 80,
    "BMC Software": 80,
    "Nielsen": 80,
    "Sprinklr": 80,
    "Zscaler": 80,
    "HighRadius": 80,
    "Darwinbox": 80,
    "Eightfold": 80,

    "Deloitte": 70,
    "Deloitte HashedIn": 70,
    "Accenture": 70,
    "IBM": 70,
    "Oracle": 70,
    "EPAM Systems": 70,
    "Persistent Systems": 70,
    "Tata Elxsi": 70,
    "Infosys": 70,
    "Wipro": 70,
    "Cognizant": 70,
    "Capgemini": 70,
    "HCL Tech": 70,
    "Tech Mahindra": 70,
    "Mphasis": 70,
    "Hexaware": 70,
    "Zensar": 70,
    "Nagarro": 70,
    "Synechron": 70,

    "BYJU'S": 60,
    "Physics Wallah": 60,
    "Unacademy": 60,
    "Testbook": 60,
    "Adda247": 60,
    "Allen": 60,
    "Coding Ninjas": 60,
    "GeeksforGeeks": 60,
    "Chegg": 60,
    "Groupon": 60,
    "MamaEarth": 60,
    "Urban Company": 60,
    "redBus": 60,
    "Cleartrip": 60
}

# -----------------------------
# Helper Functions
# -----------------------------

def get_priority(company_name: str) -> int:
    if not company_name:
        return 50
    for key in TOP_COMPANIES:
        if key.lower() in company_name.lower():
            return TOP_COMPANIES[key]
    return 50


def is_recent(posted_text: str) -> bool:
    if not posted_text:
        return False

    text = posted_text.lower()

    if "hour" in text or "today" in text:
        return True

    if "day" in text:
        try:
            return int(text.split()[0]) <= 30
        except:
            return False

    return False


# -----------------------------
# Main Fetch Function
# -----------------------------

def fetch_jobs() -> pd.DataFrame:
    url = "https://serpapi.com/search.json"
    all_jobs = []

    for role in SEARCH_ROLES:
        params = {
            "engine": "google_jobs",
            "q": role,
            "hl": "en",
            "api_key": API_KEY
        }

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        for job in data.get("jobs_results", []):
            posted = job.get("detected_extensions", {}).get("posted_at", "")

            if not is_recent(posted):
                continue

            all_jobs.append({
                "Company": job.get("company_name"),
                "Role": job.get("title"),
                "Location": job.get("location"),
                "Posted": posted,
                "Apply Link": job.get("apply_options", [{}])[0].get("link"),
                "Priority": get_priority(job.get("company_name"))
            })

    df_new = pd.DataFrame(all_jobs)

   def fetch_jobs() -> pd.DataFrame:
    url = "https://serpapi.com/search.json"
    all_jobs = []

    for role in SEARCH_ROLES:
        params = {
            "engine": "google_jobs",
            "q": role,
            "hl": "en",
            "api_key": API_KEY
        }

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        for job in data.get("jobs_results", []):
            posted = job.get("detected_extensions", {}).get("posted_at", "")

            if not is_recent(posted):
                continue

            all_jobs.append({
                "Company": job.get("company_name"),
                "Role": job.get("title"),
                "Location": job.get("location"),
                "Posted": posted,
                "Apply Link": job.get("apply_options", [{}])[0].get("link"),
                "Priority": get_priority(job.get("company_name"))
            })

    df_new = pd.DataFrame(all_jobs)

    df_new.drop_duplicates(
        subset=["Company", "Role", "Location", "Apply Link"],
        inplace=True
    )

    df_new.sort_values(by="Priority", ascending=False, inplace=True)

    return df_new


