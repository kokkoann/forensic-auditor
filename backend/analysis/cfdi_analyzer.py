from analysis.cfdi_validator import validate_cfdi
from analysis.risk_engine import calculate_risk


def analyze_cfdi(document: dict) -> dict:

    validation = validate_cfdi(
        document
    )

    findings = validation.get(
        "findings",
        []
    )

    risk = calculate_risk(
        findings
    )

    return {
        "analyzer": "CFDI_ANALYZER",
        "status": "ANALYZED",

        "summary": {
            "basic_structure_valid":
                validation.get(
                    "valid_basic_structure",
                    False
                ),

            "findings_count":
                len(findings),

            "concept_count":
                validation
                .get("cfdi_data", {})
                .get("concept_count", 0)
        },

        "risk":
            risk,

        "cfdi_data":
            validation.get(
                "cfdi_data",
                {}
            ),

        "findings":
            findings
    }