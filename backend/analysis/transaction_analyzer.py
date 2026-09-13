from normalizers.transaction_normalizer import (
    normalize_transactions
)

from analysis.money_trail import (
    detect_money_trails
)

from analysis.risk_engine import (
    calculate_risk
)


def analyze_transactions(
    document: dict
) -> dict:

    # 1. Normalizar
    normalized = normalize_transactions(
        document
    )

    if not normalized.get("normalized"):
        return {
            "analyzer":
                "TRANSACTION_ANALYZER",

            "status":
                "INVALID_SCHEMA",

            "summary": {
                "rows_analyzed": 0,
                "circular_flows": 0
            },

            "risk": {
                "score": 0,
                "level": "LOW"
            },

            "normalization":
                normalized,

            "findings": []
        }

    rows = normalized["rows"]

    # 2. Money trail
    money_findings = detect_money_trails(
        rows
    )

    # 3. Risk score
    risk = calculate_risk(
        money_findings
    )

    # 4. Resultado
    return {
        "analyzer":
            "TRANSACTION_ANALYZER",

        "status":
            "ANALYZED",

        "summary": {
            "rows_analyzed":
                len(rows),

            "circular_flows":
                len(money_findings)
        },

        "risk":
            risk,

        "normalization": {
            "column_mapping":
                normalized.get(
                    "column_mapping",
                    {}
                )
        },

        "money_trail":
            money_findings,

        "findings":
            money_findings
    }