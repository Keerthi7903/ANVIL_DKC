from google import genai

from config import settings


# Gemini Client
gemini_client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)