import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL_NAME", "models/gemini-2.5-flash")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY missing. Please check your .env file.")

client = genai.Client(api_key=API_KEY)

def summarize_timesheet(user_name, df_preview, total_hours, total_rows):
    prompt = (
        f"You are an AI productivity assistant analyzing {user_name}'s work activity.\n"
        f"Total Records: {total_rows}\nTotal Hours: {total_hours}\n"
        f"Sample Data:\n{df_preview}\n"
        "Summarize this as 4–5 concise bullet points, focusing on work balance, task types, and time distribution."
    )
    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        return resp.candidates[0].content.parts[0].text
    except Exception as e:
        return f"AI summarization failed: {e}"
