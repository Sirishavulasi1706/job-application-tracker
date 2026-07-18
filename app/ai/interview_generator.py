import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_interview_questions(company, role, job_description=""):

    prompt = f"""
You are a Senior Software Engineering Interviewer.

Generate professional interview questions for the following job.

Company: {company}

Role: {role}

Job Description:
{job_description}

Instructions:
- Return ONLY the interview preparation.
- Do NOT include introductions or conclusions.
- Do NOT use Markdown formatting.
- Do NOT indent the headings.
- Keep each question on a new line.
- Generate realistic interview questions.

Format exactly like this:

Technical Questions
1.
2.
3.
4.
5.

HR Questions
1.
2.
3.
4.

Coding Questions
1.
2.
3.

Preparation Tips
• 
• 
•
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove unnecessary blank lines
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text