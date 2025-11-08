from icalendar import Calendar
from datetime import datetime
import pandas as pd

def parse_calendar(file):
    try:
        cal = Calendar.from_ical(file.read())
        events = []
        for component in cal.walk():
            if component.name == "VEVENT":
                start = component.get("DTSTART").dt
                end = component.get("DTEND").dt
                duration = (end - start).total_seconds() / 3600
                events.append({
                    "date": start.date(),
                    "activity": component.get("SUMMARY"),
                    "type": "Calendar Event",
                    "hours": round(duration, 2),
                    "description": component.get("DESCRIPTION", "")
                })
        return pd.DataFrame(events)
    except Exception as e:
        print("Calendar Parse Error:", e)
        return pd.DataFrame()
