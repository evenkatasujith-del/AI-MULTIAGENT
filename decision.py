def make_final_decision(
    verification,
    risk,
    correction,
    re_verification
):

    # Contradiction takes priority over normal verification
    if "Potential contradiction" in risk["risks"]:

        return {
            "status": "NOT_VERIFIED",
            "confidence": verification["confidence"],
            "reason": (
                "The retrieved evidence appears to contradict the claim."
            )
        }

    # Fully supported claim
    if verification["status"] == "SUPPORTED" and not risk["risk_detected"]:

        return {
            "status": "VERIFIED",
            "confidence": verification["confidence"],
            "reason": (
                "The claim is supported by the retrieved evidence."
            )
        }

    # Re-verification after a genuine correction
    if correction["corrected"] and re_verification:

        new_verification = re_verification["verification"]

        if new_verification["status"] == "SUPPORTED":

            return {
                "status": "VERIFIED_AFTER_CORRECTION",
                "confidence": new_verification["confidence"],
                "reason": (
                    "The corrected claim passed re-verification."
                )
            }

        return {
            "status": "NOT_VERIFIED",
            "confidence": new_verification["confidence"],
            "reason": (
                "The corrected claim could not be sufficiently verified."
            )
        }

    # Partial evidence
    if verification["status"] == "PARTIALLY_SUPPORTED":

        return {
            "status": "PARTIALLY_VERIFIED",
            "confidence": verification["confidence"],
            "reason": (
                "The available evidence only partially supports the claim."
            )
        }

    # Unsupported / other cases
    return {
        "status": "NOT_VERIFIED",
        "confidence": verification["confidence"],
        "reason": verification["reason"]
    }