def verify_claim(claim, evidence):

    if evidence["status"] == "NO_EVIDENCE":
        return {
            "status": "UNSUPPORTED",
            "confidence": 0,
            "reason": "No supporting evidence was found."
        }

    if evidence["status"] == "ERROR":
        return {
            "status": "NOT_VERIFIED",
            "confidence": 0,
            "reason": "Evidence retrieval failed."
        }

    sources = evidence["sources"]

    if len(sources) >= 2:
        return {
            "status": "SUPPORTED",
            "confidence": 0.8,
            "reason": "Multiple sources were found for this claim."
        }

    return {
        "status": "PARTIALLY_SUPPORTED",
        "confidence": 0.5,
        "reason": "Only one supporting source was found."
    }