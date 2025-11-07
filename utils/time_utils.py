from dateutil import parser
import pytz

TZ = pytz.timezone("Asia/Kolkata")

def to_dt_local(ts):
    if not ts:
        return None
    try:
        dt = parser.isoparse(str(ts))
        if dt.tzinfo is None:
            return TZ.localize(dt)
        return dt.astimezone(TZ)
    except Exception:
        return None
