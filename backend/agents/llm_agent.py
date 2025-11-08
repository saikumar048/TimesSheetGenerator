# agents/llm_agent.py

from backend.llm.gemini_llm import generate_gemini_response
import json

def analyze_with_llm(agent_name: str, input_data: dict, context: str = ""):
    """
    Use Gemini to analyze uploaded data (emails, commits, calendar events).
    """
    prompt = f"""
    You are an intelligent productivity assistant named {agent_name}.
    Analyze the following JSON data which may contain calendar events, emails, and git commits.

    Consider previous context:
    {context}

    Data to analyze:
    {json.dumps(input_data, indent=2)}

    Provide:
    1. A detailed summary of work activities.
    2. Key insights or correlations.
    3. Suggestions to improve time efficiency.
    4. A motivational one-liner for the user.
    """

    return generate_gemini_response(prompt)
