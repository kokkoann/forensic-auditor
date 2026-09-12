import uuid
from pydantic import BaseModel

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from parsers.file_parser import parse_file
from agent.document_classifier import classify_document
from agent.router import route_document
from agent.ai_analyst import analyze_with_gemini

from agent.case_store import save_case, get_case
from agent.case_qa import ask_case_agent

app = FastAPI(
    title="Forensic Auditor API",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "Forensic Auditor API"
    }


@app.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):

    try:
        # 1. Leer archivo
        content = await file.read()

        # 2. Parsear archivo
        document = parse_file(
            file.filename,
            content
        )

        # 3. Clasificar documento
        classification = classify_document(
            document
        )

        # 4. Ejecutar análisis correspondiente
        analysis = route_document(
            classification["document_type"],
            document
        )

        # 5. Interpretar resultados con Gemini
        ai_report = analyze_with_gemini(
            document_type=classification["document_type"],
            analysis=analysis
        )

        case_id = str(uuid.uuid4())

        case_data = {
            "filename": file.filename,
            "classification": classification,
            "analysis": analysis,
            "ai_report": ai_report
        }

        save_case(
            case_id,
            case_data
    )

        # 6. Respuesta final
        return {
            "status": "success",
            "case_id": case_id,
            "filename": file.filename,
            "classification": classification,
            "analysis": analysis,
            "ai_report": ai_report
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc)
        }
    
class QuestionRequest(BaseModel):
    question: str

@app.post("/cases/{case_id}/ask")
def ask_case(
    case_id: str,
    request: QuestionRequest
):

    case_data = get_case(case_id)

    if not case_data:
        return {
            "status": "error",
            "message": "Caso no encontrado"
        }

    try:

        response = ask_case_agent(
            case_data=case_data,
            question=request.question
        )

        return {
            "status": "success",
            "case_id": case_id,
            "response": response
        }

    except Exception as exc:

        return {
            "status": "error",
            "message": str(exc)
        }