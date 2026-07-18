import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def optimize_resume(resume_text, job_description):

    prompt = f"""
You are an expert ATS Resume Reviewer.

Compare the resume with the job description.

Resume:

{resume_text}

Job Description:

{job_description}

Return ONLY in this exact format.

Resume Match Score
90%

Matching Skills
•
•
•

Missing Skills
•
•
•

ATS Improvements
•
•
•

Resume Improvements
•
•
•

Final Verdict
2-3 paragraphs explaining whether this resume is suitable for the job and what should be improved.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text