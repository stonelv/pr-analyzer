def compute_risk(features: dict) -> dict:
    """MVP: simple weighted rule-based risk scoring.
    features expected keys: complexity_delta, file_hotness, sensitive_path(bool), author_experience
    """
    weights = {
        "complexity_delta": 0.4,
        "file_hotness": 0.2,
        "sensitive_path": 0.3,
        "author_experience": -0.2,  # negative weight: more experience reduces risk
    }
    score = 0.0
    contributions = []
    for k, w in weights.items():
        v = features.get(k, 0)
        part = w * v
        contributions.append({"feature": k, "value": v, "weight": w, "contribution": part})
        score += part
    # Normalize to 0-1 range with simple logistic squash
    import math
    normalized = 1 / (1 + math.exp(-score))
    level = "low"
    if normalized > 0.7:
        level = "high"
    elif normalized > 0.4:
        level = "medium"
    return {"score": normalized, "level": level, "details": contributions}
