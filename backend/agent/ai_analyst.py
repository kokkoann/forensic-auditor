import os
import json
import time
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai import types
from pydantic import BaseModel


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Este archivo está en:
# backend/agent/ai_analyst.py
#
# Subimos 3 niveles para llegar a la raíz:
#
# forensic-auditor/
# ├── .env
# └── backend/
#     └── agent/
#         └── ai_analyst.py

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


# ============================================================
# MODELO DE RESPUESTA
# ============================================================

class ForensicReport(BaseModel):
    executive_summary: str
    risk_explanation: str
    key_findings: List[str]
    recommended_actions: List[str]


# ============================================================
# CREAR CLIENTE GEMINI
# ============================================================

def get_gemini_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "No se encontró GEMINI_API_KEY en el archivo .env"
        )

    client = genai.Client(
        api_key=api_key
    )

    return client


# ============================================================
# CONSTRUIR DATOS PARA GEMINI
# ============================================================

def build_payload(
    document_type: str,
    analysis: dict
) -> dict:

    return {
        "document_type": document_type,

        "risk": analysis.get(
            "risk",
            {}
        ),

        "summary": analysis.get(
            "summary",
            {}
        ),

        "findings": analysis.get(
            "findings",
            []
        )
    }


# ============================================================
# CONSTRUIR PROMPT
# ============================================================

def build_prompt(
    document_type: str,
    analysis: dict
) -> str:

    payload = build_payload(
        document_type,
        analysis
    )

    return f"""
Eres un agente especializado en auditoría financiera forense.

Tu función es interpretar evidencia que YA fue calculada por
herramientas determinísticas del sistema Forensic Auditor.

NO eres responsable de detectar nuevamente las anomalías.
NO debes modificar los resultados producidos por el sistema.

REGLAS OBLIGATORIAS:

1. Utiliza exclusivamente la evidencia proporcionada.

2. No inventes empresas, RFC, montos, fechas, transacciones
   ni relaciones.

3. No afirmes que existe fraude probado.

4. Utiliza expresiones como:
   - indicador de riesgo
   - hallazgo
   - requiere revisión
   - posible irregularidad

5. No recalcules el risk score.

6. Utiliza exactamente el risk score proporcionado
   por el sistema.

7. Si un contribuyente aparece con situación:

   "Definitivo"

   puede mencionarse como un indicador importante
   de riesgo relacionado con el Artículo 69-B.

8. Si la situación es:

   "Sentencia Favorable"

   NO debe considerarse evidencia negativa.

9. Si la situación es:

   "Desvirtuado"

   NO debe considerarse evidencia negativa.

10. Los movimientos duplicados deben describirse como
    operaciones que requieren verificación contable.

11. Los montos atípicos deben describirse como movimientos
    fuera del comportamiento esperado del documento.

12. No inventes causalidad entre diferentes hallazgos.

13. Las acciones recomendadas deben ser pasos concretos de
    auditoría o investigación.

14. La respuesta debe ser profesional, clara y breve.

15. No agregues información que no esté en los datos.

TIPO DE DOCUMENTO:

{document_type}


EVIDENCIA DEL SISTEMA:

{json.dumps(
    payload,
    ensure_ascii=False,
    indent=2
)}
"""


# ============================================================
# LLAMADA A GEMINI CON REINTENTOS
# ============================================================

def generate_with_retry(
    client,
    prompt: str,
    max_attempts: int = 3
):

    last_error = None

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(

                model="gemini-3.6-flash",

                contents=prompt,

                config=types.GenerateContentConfig(

                    response_mime_type="application/json",

                    response_schema=ForensicReport,

                    temperature=0.2
                )
            )

            return response

        # --------------------------------------------
        # Errores temporales del servidor Gemini
        # --------------------------------------------

        except errors.ServerError as exc:

            last_error = exc

            print(
                f"[Gemini] Servicio temporalmente no disponible. "
                f"Intento {attempt + 1}/{max_attempts}"
            )

            # 1s, 2s, 4s
            wait_seconds = 2 ** attempt

            print(
                f"[Gemini] Reintentando en "
                f"{wait_seconds} segundos..."
            )

            time.sleep(
                wait_seconds
            )

    # Si todos los intentos fallaron
    raise last_error


# ============================================================
# FALLBACK
# ============================================================

def generate_fallback_report(
    analysis: dict
) -> dict:

    risk = analysis.get(
        "risk",
        {}
    )

    findings = analysis.get(
        "findings",
        []
    )

    key_findings = []

    for finding in findings:

        finding_type = finding.get(
            "type",
            "UNKNOWN"
        )

        # -----------------------------------
        # SAT 69-B
        # -----------------------------------

        if finding_type == "SAT_69B":

            status = finding.get(
                "status"
            )

            rfc = finding.get(
                "rfc"
            )

            key_findings.append(
                f"RFC {rfc}: situación SAT 69-B "
                f"'{status}'."
            )

        # -----------------------------------
        # DUPLICADOS
        # -----------------------------------

        elif finding_type == "DUPLICATE_TRANSACTION":

            rfc = finding.get(
                "rfc"
            )

            cargo = finding.get(
                "cargo"
            )

            key_findings.append(
                f"Movimiento potencialmente duplicado "
                f"para RFC {rfc} por {cargo}."
            )

        # -----------------------------------
        # MONTO ATÍPICO
        # -----------------------------------

        elif finding_type == "UNUSUALLY_LARGE_AMOUNT":

            rfc = finding.get(
                "rfc"
            )

            amount = finding.get(
                "amount"
            )

            key_findings.append(
                f"Monto atípico detectado para RFC "
                f"{rfc}: {amount}."
            )

    return {

        "executive_summary": (
            "El análisis forense automático fue completado. "
            "El servicio de interpretación mediante IA no estuvo "
            "disponible temporalmente, por lo que se presenta "
            "un resumen generado directamente a partir de los "
            "hallazgos del sistema."
        ),

        "risk_explanation": (
            f"El sistema determinístico calculó un nivel de "
            f"riesgo {risk.get('level', 'UNKNOWN')} "
            f"con score {risk.get('score', 0)}/100."
        ),

        "key_findings":
            key_findings,

        "recommended_actions": [
            "Revisar manualmente los hallazgos detectados.",
            "Verificar documentación soporte de las operaciones señaladas.",
            "Revisar los RFC identificados contra las fuentes regulatorias.",
            "Reintentar posteriormente la interpretación mediante IA."
        ],

        "ai_available": False
    }


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def analyze_with_gemini(
    document_type: str,
    analysis: dict
) -> dict:

    client = get_gemini_client()

    prompt = build_prompt(
        document_type,
        analysis
    )

    try:

        # -----------------------------------
        # Gemini
        # -----------------------------------

        response = generate_with_retry(
            client,
            prompt
        )

        # -----------------------------------
        # Validar JSON generado
        # -----------------------------------

        report = ForensicReport.model_validate_json(
            response.text
        )

        result = report.model_dump()

        result["ai_available"] = True

        return result

    except Exception as exc:

        print(
            "[Gemini] No fue posible generar "
            "el reporte mediante IA."
        )

        print(
            f"[Gemini] Error: {exc}"
        )

        # -----------------------------------
        # El sistema NO se cae.
        # -----------------------------------

        return generate_fallback_report(
            analysis
        )