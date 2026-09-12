from agent.ai_analyst import analyze_with_gemini


analysis = {
    "risk": {
        "score": 90,
        "level": "HIGH"
    },

    "summary": {
        "rows_analyzed": 5,
        "sat_69b_matches": 2,
        "duplicate_transactions": 1,
        "large_amount_anomalies": 1
    },

    "findings": [
        {
            "type": "SAT_69B",
            "rfc": "AAA120730823",
            "status": "Definitivo",
            "severity": "HIGH"
        },

        {
            "type": "SAT_69B",
            "rfc": "AAA080808HL8",
            "status": "Sentencia Favorable",
            "severity": "LOW"
        },

        {
            "type": "DUPLICATE_TRANSACTION",
            "severity": "MEDIUM",
            "rfc": "BBB010101BBB",
            "cargo": 25000
        },

        {
            "type": "UNUSUALLY_LARGE_AMOUNT",
            "severity": "MEDIUM",
            "rfc": "CCC010101CCC",
            "amount": 500000
        }
    ]
}


result = analyze_with_gemini(
    document_type="ACCOUNTING_LEDGER",
    analysis=analysis
)


print(result)