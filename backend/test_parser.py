import sys
from pathlib import Path

from parsers.file_parser import parse_file
from agent.document_classifier import classify_document
from agent.router import route_document
from agent.ai_analyst import analyze_with_gemini


if len(sys.argv) < 2:
    print("Uso:")
    print("python test_parser.py ../archivo.csv")
    sys.exit(1)


file_path = Path(sys.argv[1])

if not file_path.exists():
    print(f"Archivo no encontrado: {file_path}")
    sys.exit(1)


with open(file_path, "rb") as file:
    content = file.read()


document = parse_file(
    file_path.name,
    content
)

classification = classify_document(
    document
)

analysis = route_document(
    classification["document_type"],
    document
)

ai_report = analyze_with_gemini(
    document_type=classification["document_type"],
    analysis=analysis
)


print("\n=========================")
print("CLASIFICACIÓN")
print("=========================")
print(classification)

print("\n=========================")
print("ANÁLISIS FORENSE")
print("=========================")
print(analysis)

print("\n=========================")
print("ANÁLISIS IA")
print("=========================")
print(ai_report)