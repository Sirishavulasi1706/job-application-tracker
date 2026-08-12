import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_resume(resume_text):

    prompt = f"""
You are an expert resume reviewer, ATS specialist, and career coach.

Analyze the following resume carefully.

Do NOT simply extract or rewrite the information from the resume.

Instead, evaluate the resume and provide useful career feedback.

Return the analysis using exactly these sections:

RESUME SCORE:
Give an overall score from 0 to 100 based on:
- ATS compatibility
- Skills
- Experience
- Projects
- Education
- Resume structure
- Clarity
- Relevance

STRENGTHS:
List the strongest aspects of the resume.
Give 3 to 5 specific points based only on information present in the resume.

WEAKNESSES:
Identify the most important weaknesses or missing information.
Give 3 to 5 specific points.

SKILLS ANALYSIS:
Identify the technical skills and soft skills present in the resume.
Also mention important skills that appear to be missing for the candidate's apparent career direction, but clearly label them as recommendations rather than existing skills.

PROJECT ANALYSIS:
Evaluate the projects mentioned in the resume.
Explain what is strong about them and what could be improved to make them more resume-worthy.

EXPERIENCE ANALYSIS:
Evaluate the candidate's experience.
Focus on impact, measurable achievements, responsibilities, and technical relevance.

ATS ANALYSIS:
Evaluate the resume for ATS compatibility.
Mention:
- Keywords
- Formatting
- Section structure
- Readability
- Potential ATS problems

CAREER INSIGHTS:
Provide personalized career insights based only on the candidate's resume.
Suggest suitable job roles and areas where the candidate could improve.

RECOMMENDATIONS:
Give 5 specific and actionable recommendations to improve the resume.

IMPORTANT RULES:

- Do not invent experience, education, projects, certifications, skills, achievements, or employers.
- Base your analysis only on the resume.
- If information is missing, explicitly say that it is missing.
- Do not claim that the candidate has a skill that is not present.
- Recommended skills must be clearly separated from existing skills.
- Be specific rather than generic.
- Return plain text only.
- Do not use Markdown tables.
- Do not include unnecessary introductions.

RESUME:

{resume_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text.strip()