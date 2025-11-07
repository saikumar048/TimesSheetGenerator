from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ActivityData(BaseModel):
    user: Dict[str, Any] = {"name": "User"}
    calendar: List[Dict[str, Any]] = []
    emails: List[Dict[str, Any]] = []
    git_commits: List[Dict[str, Any]] = []
