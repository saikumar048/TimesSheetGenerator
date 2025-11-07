from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd, io, os, json
from agents.ai_agent import summarize_timesheet
from utils.merge_utils import build_clean_df

load_dotenv()

app = FastAPI(title="Timesheet AI 4.1 – Enhanced")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "✅ Backend Running Successfully!"}


@app.post("/upload_files/")
async def upload_files(
    user_name: str = Form(...),
    calendar_file: UploadFile | None = None,
    email_file: UploadFile | None = None,
    git_repo_path: str | None = Form(None)
):
    try:
        calendar_text, email_df, email_json, repo_path = None, None, None, git_repo_path

        # --- Calendar (.ics) ---
        if calendar_file and calendar_file.filename.endswith(".ics"):
            calendar_text = (await calendar_file.read()).decode("utf-8")

        # --- Emails (CSV or JSON) ---
        if email_file:
            if email_file.filename.endswith(".csv"):
                email_df = pd.read_csv(email_file.file)
            elif email_file.filename.endswith(".json"):
                try:
                    email_json = json.load(email_file.file).get("emails", [])
                except Exception:
                    email_file.file.seek(0)
                    email_df = pd.read_json(email_file.file)

        # --- Merge Everything ---
        df = build_clean_df(calendar_text, email_df, email_json, repo_path)
        if df.empty:
            raise HTTPException(status_code=400, detail="No valid data found")

        buf = io.StringIO()
        df.to_csv(buf, index=False)

        ai_summary = summarize_timesheet(
            user_name,
            df.head(10).to_string(),
            df["duration_hours"].sum(),
            len(df)
        )

        return JSONResponse({
            "summary": {
                "ai_summary": ai_summary,
                "total_hours": float(df["duration_hours"].sum())
            },
            "csv_data": buf.getvalue()
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
