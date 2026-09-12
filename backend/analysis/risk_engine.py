def calculate_risk(findings: list[dict]) -> dict:
    score = 0

    for finding in findings:

        finding_type = finding.get("type")
        severity = finding.get("severity", "UNKNOWN")
        status = str(
            finding.get("status", "")
        ).strip().lower()

        # -----------------------------
        # SAT 69-B
        # -----------------------------

        if finding_type == "SAT_69B":

            if status == "definitivo":
                score += 50

            elif status == "presunto":
                score += 30

            elif status in {
                "desvirtuado",
                "sentencia favorable"
            }:
                score += 0

        # -----------------------------
        # Otros hallazgos
        # -----------------------------

        elif severity == "HIGH":
            score += 40

        elif severity == "MEDIUM":
            score += 20

        elif severity == "LOW":
            score += 5

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