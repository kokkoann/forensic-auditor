from statistics import median


def detect_duplicates(rows: list[dict]) -> list[dict]:
    """
    Detecta movimientos repetidos con la misma fecha, RFC, cargo y abono.
    """

    seen = {}
    findings = []

    for index, row in enumerate(rows):
        key = (
            str(row.get("fecha", "")).strip(),
            str(row.get("rfc", "")).strip().upper(),
            float(row.get("cargo", 0) or 0),
            float(row.get("abono", 0) or 0),
        )

        if key in seen:
            findings.append({
                "type": "DUPLICATE_TRANSACTION",
                "severity": "MEDIUM",
                "message": "Movimiento potencialmente duplicado",
                "current_row": index + 1,
                "original_row": seen[key] + 1,
                "fecha": key[0],
                "rfc": key[1],
                "cargo": key[2],
                "abono": key[3]
            })
        else:
            seen[key] = index

    return findings


from statistics import median


def detect_large_amounts(rows: list[dict]) -> list[dict]:
    """
    Detecta montos atípicos usando mediana + MAD.

    MAD = Median Absolute Deviation.
    Es más resistente a valores extremos que
    promedio + desviación estándar.
    """

    amounts = []

    for row in rows:

        cargo = float(
            row.get("cargo", 0) or 0
        )

        abono = float(
            row.get("abono", 0) or 0
        )

        amount = max(
            abs(cargo),
            abs(abono)
        )

        if amount > 0:
            amounts.append(amount)

    # Necesitamos varios movimientos
    if len(amounts) < 3:
        return []

    # -------------------------------
    # Mediana
    # -------------------------------

    med = median(amounts)

    # -------------------------------
    # MAD
    # -------------------------------

    deviations = [
        abs(amount - med)
        for amount in amounts
    ]

    mad = median(deviations)

    # Si todos los valores normales fueran
    # idénticos, evitamos threshold = mediana
    if mad == 0:
        threshold = med * 3
    else:
        threshold = med + (3 * mad)

    findings = []

    # -------------------------------
    # Detectar anomalías
    # -------------------------------

    for index, row in enumerate(rows):

        cargo = float(
            row.get("cargo", 0) or 0
        )

        abono = float(
            row.get("abono", 0) or 0
        )

        amount = max(
            abs(cargo),
            abs(abono)
        )

        if amount > threshold:

            findings.append({
                "type": "UNUSUALLY_LARGE_AMOUNT",
                "severity": "MEDIUM",
                "message": (
                    "Monto significativamente superior "
                    "al comportamiento normal del documento"
                ),
                "row": index + 1,
                "rfc": str(
                    row.get("rfc", "")
                ).strip().upper(),
                "amount": amount,
                "median": med,
                "mad": mad,
                "threshold": round(
                    threshold,
                    2
                )
            })

    return findings