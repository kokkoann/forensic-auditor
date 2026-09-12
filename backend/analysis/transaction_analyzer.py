def analyze_transactions(document: dict) -> dict:

    rows = document.get("rows", [])

    return {
        "analyzer": "TRANSACTION_ANALYZER",
        "status": "ANALYZED",
        "row_count": len(rows),
        "message": "Archivo de transacciones recibido correctamente"
    }