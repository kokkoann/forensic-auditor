cases = {}


def save_case(case_id: str, case_data: dict):
    cases[case_id] = case_data


def get_case(case_id: str):
    return cases.get(case_id)