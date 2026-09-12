import pymupdf


def parse_pdf(file_bytes: bytes) -> dict:
    document = pymupdf.open(
    stream=file_bytes,
    filetype="pdf"
)

    text = ""

    for page in document:
        text += page.get_text() + "\n"

    return {
        "format": "PDF",
        "text": text.strip()
    }