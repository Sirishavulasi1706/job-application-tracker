import json
import os

from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_job_match(resume_text, job_description):

    prompt = f"""
You are an ATS Resume Analyzer.

Compare the resume and job description.

Return ONLY valid JSON.

Format:

{{
    "match_score": 90,
    "matching_skills":[
        "Python",
        "Flask"
    ],
    "missing_skills":[
        "Docker",
        "AWS"
    ],
    "suggestions":[
        "Learn Docker",
        "Build REST APIs"
    ]
}}

Resume:

{resume_text}

Job Description:

{job_description}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    return json.loads(text)