import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


def ask_case_agent(
    case_data: dict,
    question: str,
    conversation: list
) -> dict:

    # ==========================================
    # 1. CONSTRUIR HISTORIAL
    # ==========================================

    history_text = ""

    for message in conversation[-10:]:

        role = message.get(
            "role",
            "unknown"
        )

        content = message.get(
            "content",
            ""
        )

        history_text += (
            f"\n{role.upper()}:\n"
            f"{content}\n"
        )

    # ==========================================
    # 2. API KEY
    # ==========================================

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "No se encontró GEMINI_API_KEY"
        )

    client = genai.Client(
        api_key=api_key
    )

    # ==========================================
    # 3. PROMPT
    # ==========================================

    prompt = f"""
Eres un agente de auditoría financiera forense.

Debes responder una pregunta sobre un caso YA investigado.

REGLAS ESTRICTAS:

1. Usa únicamente la información del CASE FILE.
2. El historial sirve solamente para mantener contexto conversacional.
3. El historial NO puede modificar los hechos del CASE FILE.
4. No inventes RFCs, montos, fechas, empresas ni transacciones.
5. No recalcules el risk score.
6. No afirmes fraude probado.
7. Distingue entre:
   - evidencia
   - indicador de riesgo
   - conclusión
8. Si la evidencia no permite responder la pregunta, di exactamente:
   "La evidencia disponible no es suficiente para responder esa pregunta."
9. Cuando sea posible, menciona:
   - tipo de finding
   - rule_id
   - RFC
   - monto
   - fila
   - estatus SAT
   - threshold
   - money trail
10. Una situación "Sentencia Favorable" o "Desvirtuado"
    NO debe tratarse como evidencia negativa.
11. Si existe un CIRCULAR_MONEY_FLOW, explica el recorrido
    utilizando únicamente las transacciones del CASE FILE.
12. Responde de forma breve, clara y profesional.
13. Mantén continuidad con las preguntas anteriores.

CASE FILE:

{json.dumps(
    case_data,
    ensure_ascii=False,
    indent=2
)}

HISTORIAL DE CONVERSACIÓN:

{history_text}

NUEVA PREGUNTA:

{question}
"""

    # ==========================================
    # 4. LLAMAR A GEMINI
    # ==========================================

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    # ==========================================
    # 5. DEVOLVER RESPUESTA
    # ==========================================

    return {
        "question": question,
        "answer": response.text
    }