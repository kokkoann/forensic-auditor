import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


def ask_case_agent(
    case_data: dict,
    question: str
) -> dict:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("No se encontró GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    prompt = f"""
Eres un agente de auditoría financiera forense.

Debes responder una pregunta sobre un caso YA investigado.

REGLAS ESTRICTAS:

1. Usa únicamente la información del case file.
2. No inventes RFCs, montos, fechas, empresas ni transacciones.
3. No recalcules el risk score.
4. No afirmes fraude probado.
5. Distingue entre:
   - evidencia
   - indicador de riesgo
   - conclusión
6. Si la evidencia no permite responder la pregunta, di exactamente:
   "La evidencia disponible no es suficiente para responder esa pregunta."
7. Cuando sea posible, menciona:
   - tipo de finding
   - RFC
   - monto
   - fila
   - estatus SAT
   - threshold
8. Una situación "Sentencia Favorable" o "Desvirtuado"
   NO debe tratarse como evidencia negativa.
9. Responde de forma breve, clara y profesional.

CASE FILE:

{json.dumps(case_data, ensure_ascii=False, indent=2)}

PREGUNTA DEL JUEZ:

{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return {
        "question": question,
        "answer": response.text
    }