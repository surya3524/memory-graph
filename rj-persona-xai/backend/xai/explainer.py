import math

RECOMMENDATION_TYPE_WEIGHTS = {
    "rebalancing":        {"portfolio": 1.4, "risk_profile": 1.3, "goal": 1.2, "behavior": 1.1, "life_event": 1.0, "transaction": 0.8},
    "education_funding":  {"goal": 1.4, "life_event": 1.3, "portfolio": 1.1, "risk_profile": 1.0, "behavior": 0.9, "transaction": 0.8},
    "wire_review":        {"transaction": 1.4, "behavior": 1.3, "portfolio": 1.1, "life_event": 1.0, "goal": 0.9, "risk_profile": 0.8},
    "general":            {"goal": 1.2, "portfolio": 1.2, "risk_profile": 1.1, "behavior": 1.0, "life_event": 1.0, "transaction": 0.9},
}

def _detect_recommendation_type(prompt: str) -> str:
    p = prompt.lower()
    if any(w in p for w in ["rebalanc", "drift", "allocation", "equity"]):
        return "rebalancing"
    if any(w in p for w in ["529", "education", "college", "tuition"]):
        return "education_funding"
    if any(w in p for w in ["wire", "transfer", "withdrawal"]):
        return "wire_review"
    return "general"

def compute_shap_attributions(nodes_used: list, prompt: str) -> list:
    rec_type = _detect_recommendation_type(prompt)
    weights = RECOMMENDATION_TYPE_WEIGHTS.get(rec_type, RECOMMENDATION_TYPE_WEIGHTS["general"])

    raw_scores = []
    for node in nodes_used:
        base = node["weight"]
        multiplier = weights.get(node["node_type"], 1.0)
        score = base * multiplier
        raw_scores.append((node, score))

    total = sum(s for _, s in raw_scores)
    results = []
    for node, score in raw_scores:
        pct = round((score / total) * 100, 1) if total > 0 else 0
        shap_val = round((score / total) * 2 - 1, 3)
        results.append({
            "node_id": node["node_id"],
            "label": node["label"],
            "node_type": node["node_type"],
            "shap_value": shap_val,
            "contribution_pct": pct,
            "direction": "positive" if shap_val >= 0 else "negative"
        })

    return sorted(results, key=lambda x: abs(x["shap_value"]), reverse=True)

def generate_counterfactual(nodes_used: list, prompt: str) -> str:
    rec_type = _detect_recommendation_type(prompt)
    if not nodes_used:
        return "Insufficient data to generate a counterfactual."

    top = nodes_used[0]
    t = top["node_type"]
    label = top["label"]

    if t == "portfolio":
        return f"If the portfolio equity drift were within the target band, rebalancing would not be recommended at this time."
    if t == "goal":
        val = top["value"]
        yrs = val.get("years_remaining", "?")
        return f"If the retirement timeline were 10+ years instead of {yrs}, this recommendation would shift from urgent to advisory."
    if t == "risk_profile":
        return f"If the client's risk tolerance were moderate instead of conservative, the recommended action could wait until next quarter."
    if t == "behavior":
        return f"If the client had declined prior advisor recommendations, a more cautious approach would be warranted before acting."
    if t == "life_event":
        return f"If the recent life event had not reduced household income, the recommended timeline would extend by 6–12 months."
    if t == "transaction":
        return f"If this transaction matched the client's established wire pattern in amount and destination, no additional review would be triggered."
    return f"If '{label}' were not present in the client's profile, this recommendation would change materially."

def build_xai_result(nodes_used: list, prompt: str) -> dict:
    attributions = compute_shap_attributions(nodes_used, prompt)
    counterfactual = generate_counterfactual(nodes_used, prompt)
    top_drivers = [a["label"] for a in attributions[:3]]
    top_scores = [a["contribution_pct"] for a in attributions[:3]]
    confidence = round(min(0.95, sum(top_scores[:2]) / 100 + 0.3), 2)

    return {
        "node_attributions": attributions,
        "top_drivers": top_drivers,
        "counterfactual": counterfactual,
        "confidence": confidence,
        "recommendation_type": _detect_recommendation_type(prompt)
    }
