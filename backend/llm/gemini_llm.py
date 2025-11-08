import google.generativeai as genai
import os
from dotenv import load_dotenv

# ✅ Load .env before configuration
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("🚨 No GEMINI_API_KEY found. Please add it to your .env file.")

genai.configure(api_key=api_key)

def generate_gemini_response(prompt):
    """Generate concise AI summary using Gemini."""
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini API Error: {e}"
