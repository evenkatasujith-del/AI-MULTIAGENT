def correct_claim(claim, risk):

    if not risk["risk_detected"]:
        return {
            "corrected": False,
            "original_claim": claim,
            "corrected_claim": claim,
            "reason": "No correction required."
        }

    corrected_claim = claim

    if "Unsupported claim" in risk["risks"]:
        corrected_claim = (
            "This claim could not be reliably verified because "
            "sufficient supporting evidence was not found."
        )

    return {
        "corrected": True,
        "original_claim": claim,
        "corrected_claim": corrected_claim,
        "reason": "The original claim was not sufficiently supported by evidence."
    }