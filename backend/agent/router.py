from analysis.cfdi_analyzer import analyze_cfdi
from analysis.ledger_analyzer import analyze_ledger
from analysis.transaction_analyzer import analyze_transactions


def route_document(document_type: str, document: dict) -> dict:

    if document_type == "CFDI_INVOICE":
        return analyze_cfdi(document)

    if document_type == "ACCOUNTING_LEDGER":
        return analyze_ledger(document)

    if document_type == "BANK_TRANSACTIONS":
        return analyze_transactions(document)

    return {
        "analyzer": None,
        "status": "UNSUPPORTED",
        "message": "No existe un analizador para este tipo de documento"
    }