from ..graph.sample_data import ADVISORS

def get_advisor(advisor_id: str) -> dict:
    advisor = ADVISORS.get(advisor_id)
    if not advisor:
        raise ValueError(f"Advisor {advisor_id} not found")
    return advisor

def list_advisors() -> list:
    return [
        {"advisor_id": a["advisor_id"], "name": a["name"],
         "crd": a["crd"], "branch": a["branch"]}
        for a in ADVISORS.values()
    ]
