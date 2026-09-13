import networkx as nx


def detect_money_trails(rows: list[dict]) -> list[dict]:
    """
    Detecta ciclos simples en movimientos financieros
    ya normalizados.

    Espera:
    {
        "date": ...,
        "origin": ...,
        "destination": ...,
        "amount": ...,
        "reference": ...
    }
    """

    graph = nx.DiGraph()

    # 1. Construir grafo
    for index, row in enumerate(rows):
        origin = row.get("origin")
        destination = row.get("destination")
        amount = float(row.get("amount", 0) or 0)

        if not origin or not destination:
            continue

        graph.add_edge(
            origin,
            destination,
            amount=amount,
            row=index + 1,
            date=row.get("date"),
            reference=row.get("reference")
        )

    # 2. Buscar ciclos
    cycles = list(nx.simple_cycles(graph))

    findings = []

    # 3. Convertir cada ciclo en evidencia
    for cycle in cycles:

        # MVP: ignoramos ciclos enormes
        if len(cycle) < 2 or len(cycle) > 6:
            continue

        path = []
        amounts = []

        for i in range(len(cycle)):
            origin = cycle[i]
            destination = cycle[(i + 1) % len(cycle)]

            edge = graph.get_edge_data(
                origin,
                destination
            )

            if not edge:
                continue

            amount = float(
                edge.get("amount", 0)
            )

            amounts.append(amount)

            path.append({
                "from": origin,
                "to": destination,
                "amount": amount,
                "date": edge.get("date"),
                "reference": edge.get("reference"),
                "row": edge.get("row")
            })

        if not amounts:
            continue

        starting_amount = amounts[0]
        returned_amount = amounts[-1]

        observed_difference = (
            starting_amount - returned_amount
        )

        difference_percentage = (
            (observed_difference / starting_amount) * 100
            if starting_amount > 0
            else 0
        )

        findings.append({
            "rule_id": "CIRCULAR_MONEY_FLOW",
            "type": "CIRCULAR_MONEY_FLOW",
            "severity": "HIGH",

            "message":
                "Se detectó un flujo circular de dinero.",

            "entities": cycle,

            "path": path,

            "cycle_length": len(cycle),

            "starting_amount":
                starting_amount,

            "returned_amount":
                returned_amount,

            "observed_difference":
                observed_difference,

            "difference_percentage":
                round(
                    difference_percentage,
                    2
                )
        })

    return findings