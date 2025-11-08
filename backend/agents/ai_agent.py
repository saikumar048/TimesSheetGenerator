import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = os.getenv("MODEL_NAME", "models/gemini-2.5-flash")

def summarize_timesheet(df):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""
        You are an AI productivity coach.
        Analyze this timesheet:
        {df.to_string(index=False)}
        Summarize key productivity trends, list 3 insights, and suggest 3 time management tips.
        Keep it short and professional.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini API Error: {e}"
