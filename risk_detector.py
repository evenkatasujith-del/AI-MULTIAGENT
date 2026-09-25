def detect_risk(claim, verification):

    risks = []

    if verification["status"] == "UNSUPPORTED":
        risks.append("Unsupported claim")

    if verification["confidence"] < 0.5:
        risks.append("Low confidence")

    if verification["status"] == "PARTIALLY_SUPPORTED":
        risks.append("Insufficient supporting evidence")

    if risks:
        return {
            "risk_detected": True,
            "risks": risks
        }

    return {
        "risk_detected": False,
        "risks": []
    }