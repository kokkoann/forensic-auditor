import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Cargar .env de la raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("No se encontró GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Responde únicamente: CONEXION EXITOSA"
)


print(response.text)