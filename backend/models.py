from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class TimesheetEntry(Base):
    __tablename__ = "timesheet_entries"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    day = Column(String)
    activity_type = Column(String, index=True)
    description = Column(String)
    start_time_local = Column(String)
    end_time_local = Column(String)
    duration_minutes = Column(Integer)
    duration_hours = Column(Float)
    source_id = Column(String, index=True)
    tags = Column(String)
    notes = Column(String)
