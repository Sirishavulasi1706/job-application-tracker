import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_career_insights(analysis):

    prompt = f"""
You are a professional career coach.

Based on this resume analysis:

{analysis}

Return ONLY in this format.

Resume Score:
Resume Strength:
Top Skills:
Missing Skills:
Recommended Role:
Advice:

Resume Score should be out of 100.
Resume Strength should be from 1 to 5 stars.
Top Skills should contain at most 5 skills.
Missing Skills should contain at most 5 skills.
Advice should be short.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text