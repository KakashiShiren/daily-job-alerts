import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ========== ENV VARIABLES ==========
FROM_EMAIL = os.environ["FROM_EMAIL"]
APP_PASSWORD = os.environ["APP_PASSWORD"]
SERPAPI_KEY = os.environ["SERPAPI_KEY"]
TO_EMAIL = "tarunreddy2811@gmail.com"

# ========== SEARCH CONFIG ==========
QUERIES = [
    "entry level software engineer new grad remote",
    "entry level data scientist remote",
    "entry level data analyst remote",
    "entry level machine learning engineer new grad"
]

EXCLUDE_KEYWORDS = [
    "2+ years", "3+ years", "4+ years",
    "minimum 2 years", "at least 2 years",
    "senior", "staff", "lead", "mid-level"
]

# ========== FUNCTIONS ==========
def fetch_jobs(query):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_jobs",
        "q": query,
        "api_key": SERPAPI_KEY
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json().get("jobs_results", [])

def is_entry_level(job):
    text = (job.get("description") or "").lower()
    return not any(keyword in text for keyword in EXCLUDE_KEYWORDS)

def build_email(jobs):
    today = datetime.now().date()
    html = f"<h2>Daily Entry-Level Job Alerts – {today}</h2>"
    html += "<p><b>Strictly 0–1 YOE · Remote included</b></p><hr>"

    if not jobs:
        html += "<p>No qualifying new jobs found today.</p>"
        return html

    for job in jobs:
        html += f"""
        <p>
        <b>{job.get('title')}</b><br>
        Company: {job.get('company_name')}<br>
        Location: {job.get('location')}<br>
        <a href="{job.get('link')}" target="_blank">Apply here</a>
        </p>
        <hr>
        """
    return html

# ========== MAIN ==========
all_jobs = []

for query in QUERIES:
    try:
        results = fetch_jobs(query)
        for job in results:
            if is_entry_level(job):
                all_jobs.append(job)
    except Exception as e:
        print("Error fetching jobs:", e)

email_html = build_email(all_jobs)

msg = MIMEText(email_html, "html")
msg["Subject"] = "Daily REAL Entry-Level Job Alerts (0–1 YOE)"
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(FROM_EMAIL, APP_PASSWORD)
    server.send_message(msg)

print("Email sent successfully")
