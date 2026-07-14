import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_resume(resume_text):

    prompt = f"""
You are an expert resume analyzer.

Analyze the following resume.

Return ONLY the result in this format.

Name:
Email:
Education:
Skills:
Projects:
Experience:
Certifications:

Resume:

{resume_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text