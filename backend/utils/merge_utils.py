import pandas as pd
from backend.utils.calendar_utils import parse_calendar
from backend.utils.mail_utils import parse_emails
from backend.utils.git_utils import parse_git

def build_clean_df(calendar_file=None, email_file=None, repo_path=None):
    dfs = []

    if calendar_file:
        dfs.append(parse_calendar(calendar_file))

    if email_file:
        dfs.append(parse_emails(email_file))

    if repo_path:
        dfs.append(parse_git(repo_path))

    if not dfs:
        return pd.DataFrame()

    df = pd.concat(dfs, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df["hours"] = df["hours"].fillna(0)
    return df.sort_values("date")
