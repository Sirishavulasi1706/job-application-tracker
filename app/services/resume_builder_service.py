from app.services.ai_client import generate_text


def generate_resume(
    full_name,
    email,
    phone,
    linkedin,
    github,
    portfolio,
    education,
    skills,
    experience,
    projects,
    certifications,
    achievements
):

    prompt = f"""
You are an expert resume writer.

Generate a professional ATS-friendly resume.

Candidate Information

Full Name:
{full_name}

Email:
{email}

Phone:
{phone}

LinkedIn:
{linkedin}

GitHub:
{github}

Portfolio:
{portfolio}

Education:
{education}

Skills:
{skills}

Experience:
{experience}

Projects:
{projects}

Certifications:
{certifications}

Achievements:
{achievements}

Instructions:

- Produce a professional resume.
- Use proper headings.
- Improve grammar.
- Do not invent experience.
- Make it ATS friendly.
- Keep formatting clean.
- Return plain text only.
"""

    return generate_text(prompt)