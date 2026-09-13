from normalizers.transaction_normalizer import (
    is_transaction_document
)


def normalize_columns(columns):
    """
    Convierte los nombres de columnas a minúsculas
    y elimina espacios.
    """
    return {
        str(column).strip().lower()
        for column in columns
    }


def classify_document(document: dict) -> dict:

    file_format = document.get("format", "")

    # ==========================================
    # CSV / EXCEL
    # ==========================================

    if file_format in {"CSV", "EXCEL"}:

        original_columns = document.get(
            "columns",
            []
        )

        columns = normalize_columns(
            original_columns
        )

        # --------------------------------------
        # 1. Detectar libro contable
        # --------------------------------------

        ledger_keywords = {
            "cuenta",
            "concepto",
            "cargo",
            "abono",
            "saldo"
        }

        ledger_matches = len(
            columns & ledger_keywords
        )

        if ledger_matches >= 3:
            return {
                "document_type": "ACCOUNTING_LEDGER",
                "confidence": 0.90,
                "reason": (
                    f"Se encontraron {ledger_matches} "
                    "columnas compatibles con un libro contable."
                )
            }

        # --------------------------------------
        # 2. Detectar archivo de transacciones
        #    usando el normalizador
        # --------------------------------------

        is_transaction, transaction_mapping = (
            is_transaction_document(
                original_columns
            )
        )

        if is_transaction:
            return {
                "document_type": "BANK_TRANSACTIONS",
                "confidence": 0.90,
                "reason": (
                    "Se identificaron columnas compatibles "
                    "con movimientos financieros."
                ),
                "column_mapping":
                    transaction_mapping
            }

    # ==========================================
    # XML
    # ==========================================

    if file_format == "XML":

        root_tag = str(
            document.get("root_tag", "")
        ).lower()

        xml_text = str(
            document.get("xml_text", "")
        ).lower()

        if (
            "comprobante" in root_tag
            or "cfdi" in xml_text
        ):
            return {
                "document_type": "CFDI_INVOICE",
                "confidence": 0.99,
                "reason": (
                    "El XML contiene elementos "
                    "característicos de un CFDI."
                )
            }

    # ==========================================
    # PDF
    # ==========================================

    if file_format == "PDF":

        text = str(
            document.get("text", "")
        ).lower()

        invoice_keywords = {
            "cfdi",
            "factura",
            "rfc",
            "uuid",
            "subtotal",
            "total"
        }

        matches = sum(
            keyword in text
            for keyword in invoice_keywords
        )

        if matches >= 3:
            return {
                "document_type": "CFDI_INVOICE",
                "confidence": 0.80,
                "reason": (
                    f"Se encontraron {matches} "
                    "indicadores relacionados con una factura."
                )
            }

    # ==========================================
    # DESCONOCIDO
    # ==========================================

    return {
        "document_type": "UNKNOWN",
        "confidence": 0.0,
        "reason": (
            "No se encontraron suficientes indicadores "
            "para clasificar el documento."
        )
    }