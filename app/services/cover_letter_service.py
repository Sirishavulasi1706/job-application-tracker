from app.services.ai_client import generate_text


def generate_cover_letter(company, role, job_description):

    prompt = f"""
You are an expert career coach and professional recruiter.

Write a modern, ATS-friendly cover letter for the following job.

Company:
{company}

Role:
{role}

Job Description:
{job_description}

Requirements:

- Write in a professional, natural tone.
- Keep it between 300 and 400 words.
- Personalize it for the company and role.
- Highlight problem-solving, teamwork, adaptability, and enthusiasm.
- Do NOT invent experiences or skills that are not provided.
- Start directly with:
  Dear Hiring Manager,
- End with a professional closing.
- Return plain text only.

Do NOT include:
- [Your Name]
- [Your Address]
- [Your Phone Number]
- [Your Email]
- [Date]
- Placeholder text of any kind
- Markdown formatting such as **bold** or bullet points unless absolutely necessary.
"""

    return generate_text(prompt)