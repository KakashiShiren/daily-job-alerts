import smtplib
import requests
import os
from email.mime.text import MIMEText
from datetime import datetime

TO_EMAIL = "tarunreddy2811@gmail.com"
FROM_EMAIL = os.environ["FROM_EMAIL"]
APP_PASSWORD = os.environ["APP_PASSWORD"]

SEARCH_TERMS = [
    "entry level software engineer new grad remote",
    "entry level data scientist remote",
    "entry level data analyst remote",
    "entry level machine learning engineer new grad"
]

def build_email():
    html = f"<h2>Daily Entry-Level Job Alerts – {datetime.now().date()}</h2>"
    html += "<p>New entry-level / new-grad roles (0–1 YOE only, remote included)</p><ul>"

    for term in SEARCH_TERMS:
        link = f"https://www.google.com/search?q={term.replace(' ', '+')}"
        html += f"<li><a href='{link}' target='_blank'>{term}</a></li>"

    html += "</ul>"
    return html

msg = MIMEText(build_email(), "html")
msg["Subject"] = "Daily Entry-Level Job Alerts (0–1 YOE)"
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(FROM_EMAIL, APP_PASSWORD)
    server.send_message(msg)

print("Email sent successfully")
