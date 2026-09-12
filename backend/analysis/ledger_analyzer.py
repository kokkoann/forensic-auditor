from analysis.risk_engine import calculate_risk
from analysis.blacklist_69b import check_rfc_69b
from analysis.anomalies import (
    detect_duplicates,
    detect_large_amounts
)


def analyze_ledger(document: dict) -> dict:

    rows = document.get("rows", [])

    rfcs = set()

    for row in rows:
        rfc = row.get("rfc")

        if rfc:
            rfc = str(rfc).strip().upper()

            if rfc:
                rfcs.add(rfc)

    # -----------------------------
    # SAT 69-B
    # -----------------------------

    sat_findings = []

    for rfc in rfcs:
        result = check_rfc_69b(rfc)

        if result["found"]:
            sat_findings.append(result)

    # -----------------------------
    # Duplicados
    # -----------------------------

    duplicate_findings = detect_duplicates(rows)

    # -----------------------------
    # Montos anómalos
    # -----------------------------

    amount_findings = detect_large_amounts(rows)

    # -----------------------------
    # Consolidar findings
    # -----------------------------

    findings = (
        sat_findings
        + duplicate_findings
        + amount_findings
    )

    # -----------------------------
    # Risk score
    # -----------------------------

    risk = calculate_risk(findings)

    high_risk_findings = [
        finding
        for finding in findings
        if finding.get("severity") == "HIGH"
    ]

    medium_risk_findings = [
        finding
        for finding in findings
        if finding.get("severity") == "MEDIUM"
    ]

    return {
        "analyzer": "LEDGER_ANALYZER",
        "status": "ANALYZED",

        "summary": {
            "rows_analyzed": len(rows),
            "unique_rfcs": len(rfcs),
            "sat_69b_matches": len(sat_findings),
            "duplicate_transactions": len(duplicate_findings),
            "large_amount_anomalies": len(amount_findings),
            "high_risk_findings": len(high_risk_findings),
            "medium_risk_findings": len(medium_risk_findings)
        },

        "risk": risk,

        "rfcs_analyzed": sorted(rfcs),

        "findings": findings
    }