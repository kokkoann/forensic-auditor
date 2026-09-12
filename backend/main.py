from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from parsers.file_parser import parse_file
from agent.document_classifier import classify_document
from agent.router import route_document
from agent.ai_analyst import analyze_with_gemini


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

        # 6. Respuesta final
        return {
            "status": "success",
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