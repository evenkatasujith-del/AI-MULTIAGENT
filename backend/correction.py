def correct_claim(claim, risk):
    risks = risk.get("risks", [])

    # No risk → claim does not need correction
    if not risk.get("risk_detected"):
        return {
            "corrected": False,
            "action": "ACCEPT",
            "original_claim": claim,
            "corrected_claim": claim,
            "reason": "No correction required."
        }

    # Contradiction → reject the claim
    if "Potential contradiction" in risks:
        return {
            "corrected": True,
            "action": "REJECT",
            "original_claim": claim,
            "corrected_claim": None,
            "reason": (
                "The claim conflicts with the available evidence "
                "and was rejected."
            )
        }

    # No supporting evidence → reject the claim
    if "Unsupported claim" in risks or "No evidence found" in risks:
        return {
            "corrected": True,
            "action": "REJECT",
            "original_claim": claim,
            "corrected_claim": None,
            "reason": (
                "The claim was not sufficiently supported by "
                "the available evidence and was rejected."
            )
        }

    # Partial evidence → keep it but flag it
    if "Insufficient supporting evidence" in risks:
        return {
            "corrected": True,
            "action": "QUALIFY",
            "original_claim": claim,
            "corrected_claim": claim,
            "reason": (
                "The claim has only partial supporting evidence "
                "and should not be treated as fully verified."
            )
        }

    # Other verification problems
    return {
        "corrected": False,
        "action": "REVIEW",
        "original_claim": claim,
        "corrected_claim": claim,
        "reason": (
            "The claim requires additional evidence before "
            "it can be reliably accepted."
        )
    }