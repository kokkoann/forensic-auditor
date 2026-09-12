from parsers.csv_parser import parse_csv
from parsers.excel_parser import parse_excel
from parsers.pdf_parser import parse_pdf
from parsers.xml_parser import parse_xml


SUPPORTED_EXTENSIONS = {
    "csv",
    "xlsx",
    "xls",
    "pdf",
    "xml"
}


def get_extension(filename: str) -> str:
    if "." not in filename:
        return ""

    return filename.rsplit(".", 1)[1].lower()


def parse_file(filename: str, file_bytes: bytes) -> dict:
    extension = get_extension(filename)

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Formato no soportado: {extension}"
        )

    if extension == "csv":
        return parse_csv(file_bytes)

    if extension in ("xlsx", "xls"):
        return parse_excel(file_bytes)

    if extension == "pdf":
        return parse_pdf(file_bytes)

    if extension == "xml":
        return parse_xml(file_bytes)

    raise ValueError("No se pudo procesar el archivo")