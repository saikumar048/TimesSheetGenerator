from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import pandas as pd
import os
from backend.utils.merge_utils import build_clean_df
from backend.agents.ai_agent import summarize_timesheet

app = FastAPI(title="AI Timesheet Analyzer API")

@app.get("/")
def home():
    return {"message": "✅ Backend API is running successfully!"}

@app.post("/process")
async def process_data(
    calendar_file: UploadFile = None,
    email_file: UploadFile = None,
    repo_path: str = Form(None)
):
    df = build_clean_df(
        calendar_file.file if calendar_file else None,
        email_file.file if email_file else None,
        repo_path
    )

    if df.empty:
        return JSONResponse({"detail": "No valid data aggregated"}, status_code=400)

    os.makedirs("outputs", exist_ok=True)
    csv_path = "outputs/aggregated_timesheet.csv"
    df.to_csv(csv_path, index=False)

    ai_summary = summarize_timesheet(df)
    total_hours = df["hours"].sum()

    return {"csv_path": csv_path, "ai_summary": ai_summary, "total_hours": total_hours}
