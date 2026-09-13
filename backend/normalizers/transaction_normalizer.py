import re
import unicodedata


COLUMN_ALIASES = {
    "date": {
        "fecha",
        "fecha_operacion",
        "fecha_transaccion",
        "fecha_movimiento",
        "date",
        "transaction_date",
    },

    "origin": {
        "origen",
        "cuenta_origen",
        "cuenta_ordenante",
        "ordenante",
        "emisor",
        "sender",
        "source",
        "origin",
        "source_account",
    },

    "destination": {
        "destino",
        "cuenta_destino",
        "cuenta_beneficiario",
        "beneficiario",
        "receptor",
        "receiver",
        "destination",
        "destination_account",
    },

    "amount": {
        "monto",
        "importe",
        "cantidad",
        "valor",
        "amount",
        "transaction_amount",
    },

    "reference": {
        "referencia",
        "concepto",
        "descripcion",
        "reference",
        "description",
    },
}


def normalize_column_name(value):
    """
    Ejemplo:
    'Cuenta Ordenante' -> 'cuenta_ordenante'
    """

    value = str(value).strip().lower()

    value = unicodedata.normalize(
        "NFKD",
        value
    )

    value = "".join(
        char
        for char in value
        if not unicodedata.combining(char)
    )

    value = re.sub(
        r"[^a-z0-9]+",
        "_",
        value
    )

    return value.strip("_")


def detect_transaction_columns(columns):
    """
    Descubre qué columnas del archivo representan
    fecha, origen, destino, monto y referencia.
    """

    normalized_columns = {
        normalize_column_name(column): column
        for column in columns
    }

    mapping = {}

    for canonical_name, aliases in COLUMN_ALIASES.items():

        for alias in aliases:

            normalized_alias = normalize_column_name(alias)

            if normalized_alias in normalized_columns:

                mapping[canonical_name] = (
                    normalized_columns[normalized_alias]
                )

                break

    return mapping


def normalize_transactions(document):
    """
    Convierte un documento de transacciones
    a nuestro formato interno estándar.
    """

    columns = document.get("columns", [])
    rows = document.get("rows", [])

    mapping = detect_transaction_columns(columns)

    required = {
        "origin",
        "destination",
        "amount"
    }

    # Si faltan columnas indispensables
    if not required.issubset(mapping.keys()):

        missing = [
            field
            for field in required
            if field not in mapping
        ]

        return {
            "normalized": False,
            "column_mapping": mapping,
            "missing_fields": missing,
            "rows": []
        }

    normalized_rows = []

    for row in rows:

        origin = row.get(
            mapping["origin"]
        )

        destination = row.get(
            mapping["destination"]
        )

        amount = row.get(
            mapping["amount"]
        )

        date = (
            row.get(mapping["date"])
            if "date" in mapping
            else None
        )

        reference = (
            row.get(mapping["reference"])
            if "reference" in mapping
            else None
        )

        try:
            amount = float(amount or 0)

        except (TypeError, ValueError):
            amount = 0.0

        if not origin or not destination:
            continue

        normalized_rows.append({
            "date":
                str(date).strip()
                if date is not None
                else None,

            "origin":
                str(origin).strip().upper(),

            "destination":
                str(destination).strip().upper(),

            "amount":
                amount,

            "reference":
                str(reference).strip()
                if reference is not None
                else None
        })

    return {
        "normalized": True,
        "column_mapping": mapping,
        "row_count": len(normalized_rows),
        "rows": normalized_rows
    }

def is_transaction_document(columns: list[str]) -> tuple[bool, dict]:
    mapping = detect_transaction_columns(columns)

    required = {
        "origin",
        "destination",
        "amount"
    }

    detected = required.issubset(
        mapping.keys()
    )

    return detected, mapping