cases = {}


def save_case(case_id: str, case_data: dict):
    cases[case_id] = {
        "case_data": case_data,
        "conversation": []
    }


def get_case(case_id: str):
    return cases.get(case_id)


def add_message(
    case_id: str,
    role: str,
    content: str
):
    case = cases.get(case_id)

    if not case:
        return False

    case["conversation"].append({
        "role": role,
        "content": content
    })

    return True


def get_conversation(case_id: str):
    case = cases.get(case_id)

    if not case:
        return []

    return case.get(
        "conversation",
        []
    )