import pandas as pd
from dateutil import parser
import pytz
from ics import Calendar
from io import StringIO
import git
import os

TZ = pytz.timezone("Asia/Kolkata")

# --- Helper ---
def safe_parse_date(ts):
    if not ts or str(ts).strip() == "":
        return None
    try:
        dt = parser.parse(str(ts), fuzzy=True)
        if dt.tzinfo is None:
            dt = TZ.localize(dt)
        return dt.astimezone(TZ)
    except Exception:
        return None


# --- Calendar Parser ---
def parse_ics_file(ics_text):
    rows = []
    try:
        cal = Calendar(ics_text)
    except Exception:
        cal = Calendar(StringIO(ics_text).read())

    for event in cal.events:
        start = event.begin.astimezone(TZ)
        end = event.end.astimezone(TZ)
        dur = (end - start).total_seconds() / 3600
        rows.append({
            "date": start.date().isoformat(),
            "type": "Calendar",
            "desc": event.name or "Meeting/Event",
            "start_time": start.strftime("%H:%M"),
            "end_time": end.strftime("%H:%M"),
            "duration_hours": round(dur, 2)
        })
    return rows


# --- Git Parser ---
def parse_git_commits(repo_path):
    repo = git.Repo(repo_path)
    commits = list(repo.iter_commits(max_count=30))
    rows = []
    for c in commits:
        ts = c.committed_datetime.astimezone(TZ)
        rows.append({
            "date": ts.date().isoformat(),
            "type": "Git Commit",
            "desc": c.message.strip().split("\n")[0],
            "start_time": ts.strftime("%H:%M"),
            "end_time": "",
            "duration_hours": 0.25
        })
    return rows


# --- Email Parser for CSV ---
def parse_email_file(email_df):
    rows = []
    for _, r in email_df.iterrows():
        ts = safe_parse_date(r.get("timestamp") or r.get("date"))
        if not ts:
            continue
        rows.append({
            "date": ts.date().isoformat(),
            "type": "Email",
            "desc": r.get("subject", "Email message"),
            "start_time": ts.strftime("%H:%M"),
            "end_time": "",
            "duration_hours": 0.1
        })
    return rows


# --- Email Parser for JSON ---
def parse_email_json(email_data):
    rows = []
    for email in email_data:
        ts = safe_parse_date(email.get("date") or email.get("timestamp"))
        if not ts:
            continue
        desc = email.get("subject", "No Subject")
        sender = email.get("from", "")
        labels = ", ".join(email.get("labels", []))
        priority = email.get("priority", "normal")
        attachments = len(email.get("attachments", []))
        rows.append({
            "date": ts.date().isoformat(),
            "type": "Email",
            "desc": f"{desc} | From: {sender} | Priority: {priority} | Labels: {labels} | Attachments: {attachments}",
            "start_time": ts.strftime("%H:%M"),
            "end_time": "",
            "duration_hours": 0.1
        })
    return rows


# --- Unified Merge ---
def build_clean_df(calendar_text=None, email_df=None, email_json=None, repo_path=None):
    rows = []

    if calendar_text:
        rows += parse_ics_file(calendar_text)

    if repo_path and os.path.exists(repo_path):
        rows += parse_git_commits(repo_path)

    if email_df is not None and not email_df.empty:
        rows += parse_email_file(email_df)

    if email_json:
        rows += parse_email_json(email_json)

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["duration_hours"] = df["duration_hours"].fillna(0)
    df = df.sort_values(["date", "start_time"]).reset_index(drop=True)
    return df
