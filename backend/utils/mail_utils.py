import pandas as pd
import json
from datetime import datetime

def parse_emails(file):
    try:
        data = json.load(file)
        emails = []
        for mail in data.get("emails", []):
            date_str = mail.get("date")
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            emails.append({
                "date": dt.date(),
                "activity": mail.get("subject", "No Subject"),
                "type": "Email",
                "hours": 0.5,
                "description": mail.get("body", "")[:150]
            })
        return pd.DataFrame(emails)
    except Exception as e:
        print("Email Parse Error:", e)
        return pd.DataFrame()
