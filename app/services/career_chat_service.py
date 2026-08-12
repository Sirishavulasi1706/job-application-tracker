from app.services.ai_client import generate_text


def ask_career_assistant(message):

    prompt = f"""
You are an expert AI Career Assistant.

Help users with:

- Resume reviews
- Career guidance
- Interview preparation
- Salary negotiation
- Technical interviews
- HR interviews
- Cover letters
- Job searching

User Question:

{message}

Return a helpful professional answer.
"""

    return generate_text(prompt)