from google import genai
from config import Config

client = genai.Client(
    api_key=Config.GEMINI_API_KEY
)

MODEL = "gemini-2.5-flash"


def generate_text(prompt: str) -> str:
    """
    Generates plain text using Gemini.
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text.strip()