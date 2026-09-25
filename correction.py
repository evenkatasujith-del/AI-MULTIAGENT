def correct_claim(claim, risk):

    if not risk["risk_detected"]:
        return {
            "corrected": False,
            "original_claim": claim,
            "corrected_claim": claim,
            "reason": "No correction required."
        }

    if "Unsupported claim" in risk["risks"]:

        return {
            "corrected": True,
            "original_claim": claim,
            "corrected_claim": (
                "This claim is not sufficiently supported by the available evidence."
            ),
            "reason": (
                "The original claim was not sufficiently supported "
                "by reliable evidence."
            )
        }

    if "Insufficient supporting evidence" in risk["risks"]:

        return {
            "corrected": False,
            "original_claim": claim,
            "corrected_claim": claim,
            "reason": (
                "The claim is only partially supported by the available evidence, "
                "so it was not rewritten without stronger evidence."
            )
        }

    return {
        "corrected": False,
        "original_claim": claim,
        "corrected_claim": claim,
        "reason": "The claim could not be reliably verified."
    }