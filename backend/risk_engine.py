
def calculate_risk(findings: list[dict]) -> dict:
    score = 0

    weights = {
        "HIGH": 40,
        "MEDIUM": 20,
        "LOW": 5,
        "NONE": 0,
        "UNKNOWN": 0
    }

    for finding in findings:
        severity = finding.get("severity", "UNKNOWN")

        score += weights.get(
            severity,
            0
        )

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"

    elif score >= 40:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "score": score,
        "level": level
    }