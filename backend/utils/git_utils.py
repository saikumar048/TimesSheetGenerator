import subprocess
import pandas as pd
from datetime import datetime

def parse_git(repo_path):
    if not repo_path or not isinstance(repo_path, str):
        return pd.DataFrame()

    try:
        git_log = subprocess.check_output(
            ["git", "-C", repo_path, "log", "--pretty=format:%ad|%s", "--date=iso"],
            text=True
        )
        commits = []
        for line in git_log.split("\n"):
            if "|" in line:
                dt_str, msg = line.split("|", 1)
                dt = datetime.fromisoformat(dt_str.strip())
                commits.append({
                    "date": dt.date(),
                    "activity": msg.strip(),
                    "type": "Git Commit",
                    "hours": 1.0,
                    "description": "Code commit"
                })
        return pd.DataFrame(commits)
    except Exception as e:
        print("Git Parse Error:", e)
        return pd.DataFrame()
