import uuid

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from parsers.file_parser import parse_file
from agent.document_classifier import classify_document
from agent.router import route_document
from agent.ai_analyst import analyze_with_gemini

from agent.case_store import (
    save_case,
    get_case,
    add_message,
    get_conversation
)

from agent.case_qa import ask_case_agent


# ==========================================
# REQUEST MODELS
# ==========================================

class QuestionRequest(BaseModel):
    question: str


# ==========================================
# FASTAPI
# ==========================================

app = FastAPI(
    title="Forensic Auditor API",
    version="0.1.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def health_check():

    return {
        "status": "ok",
        "service": "Forensic Auditor API"
    }


# ==========================================
# ANALIZAR DOCUMENTO
# ==========================================

@app.post("/analyze-document")
async def analyze_document(
    file: UploadFile = File(...)
):

    try:

        # ----------------------------------
        # 1. Leer archivo
        # ----------------------------------

        content = await file.read()

        # ----------------------------------
        # 2. Parsear
        # ----------------------------------

        document = parse_file(
            file.filename,
            content
        )

        # ----------------------------------
        # 3. Clasificar
        # ----------------------------------

        classification = classify_document(
            document
        )

        # ----------------------------------
        # 4. Análisis forense
        # ----------------------------------

        analysis = route_document(
            classification["document_type"],
            document
        )

        # ----------------------------------
        # 5. Interpretación IA
        # ----------------------------------

        ai_report = analyze_with_gemini(
            document_type=
                classification["document_type"],

            analysis=analysis
        )

        # ----------------------------------
        # 6. Crear caso
        # ----------------------------------

        case_id = str(
            uuid.uuid4()
        )

        case_data = {
            "filename":
                file.filename,

            "classification":
                classification,

            "analysis":
                analysis,

            "ai_report":
                ai_report
        }

        save_case(
            case_id,
            case_data
        )

        # ----------------------------------
        # 7. Respuesta
        # ----------------------------------

        return {
            "status":
                "success",

            "case_id":
                case_id,

            "filename":
                file.filename,

            "classification":
                classification,

            "analysis":
                analysis,

            "ai_report":
                ai_report
        }

    except Exception as exc:

        return {
            "status":
                "error",

            "message":
                str(exc)
        }


# ==========================================
# PREGUNTAR SOBRE UN CASO
# ==========================================

@app.post("/cases/{case_id}/ask")
def ask_case(
    case_id: str,
    request: QuestionRequest
):

    case = get_case(
        case_id
    )

    if not case:

        return {
            "status": "error",
            "message": "Caso no encontrado"
        }

    # Nuestro case_store guarda:
    #
    # {
    #     "case_data": {...},
    #     "conversation": [...]
    # }

    case_data = case[
        "case_data"
    ]

    conversation = get_conversation(
        case_id
    )

    try:

        response = ask_case_agent(
            case_data=case_data,
            question=request.question,
            conversation=conversation
        )

        # Guardar pregunta
        add_message(
            case_id,
            "user",
            request.question
        )

        # Guardar respuesta
        add_message(
            case_id,
            "assistant",
            response["answer"]
        )

        return {
            "status":
                "success",

            "case_id":
                case_id,

            "response":
                response
        }

    except Exception as exc:

        return {
            "status":
                "error",

            "message":
                str(exc)
        }


# ==========================================
# CONSULTAR HISTORIAL DEL CASO
# ==========================================

@app.get("/cases/{case_id}/conversation")
def get_case_conversation_endpoint(
    case_id: str
):

    case = get_case(
        case_id
    )

    if not case:

        return {
            "status": "error",
            "message": "Caso no encontrado"
        }

    return {
        "status":
            "success",

        "case_id":
            case_id,

        "conversation":
            get_conversation(
                case_id
            )
    }