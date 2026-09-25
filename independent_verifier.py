def independent_verify(claim, evidence):

    claim_lower = claim.lower()

    # No evidence available
    if evidence.get("status") != "EVIDENCE_FOUND":
        return {
            "status": "NOT_VERIFIED",
            "confidence": 0.0,
            "reason": "Independent verification could not find supporting evidence."
        }

    evidence_text = " ".join(
        source.get("evidence", "")
        for source in evidence.get("sources", [])
    ).lower()

    # Detect direct contradiction
    contradiction_pairs = [
        ("is not", "is"),
        ("was not", "was"),
        ("does not", "does"),
        ("cannot", "can"),
        ("never", "always")
    ]

    for negative, positive in contradiction_pairs:

        if negative in claim_lower and positive in evidence_text:
            return {
                "status": "CONTRADICTED",
                "confidence": 0.95,
                "reason": "The evidence contains information that conflicts with the claim."
            }

        if positive in claim_lower and negative in evidence_text:
            return {
                "status": "CONTRADICTED",
                "confidence": 0.95,
                "reason": "The evidence contains information that conflicts with the claim."
            }

    # Independent keyword check
    claim_words = [
        word.strip(".,!?")
        for word in claim_lower.split()
        if len(word.strip(".,!?")) > 3
    ]

    if not claim_words:
        return {
            "status": "NOT_VERIFIED",
            "confidence": 0.0,
            "reason": "The claim could not be independently analyzed."
        }

    matched_words = sum(
        1 for word in claim_words
        if word in evidence_text
    )

    ratio = matched_words / len(claim_words)

    if ratio >= 0.7:
        return {
            "status": "INDEPENDENTLY_SUPPORTED",
            "confidence": round(ratio, 2),
            "reason": "The independent verification path found strong evidence for the claim."
        }

    if ratio >= 0.4:
        return {
            "status": "INDEPENDENTLY_PARTIAL",
            "confidence": round(ratio, 2),
            "reason": "The independent verification path found partial evidence."
        }

    return {
        "status": "NOT_VERIFIED",
        "confidence": round(ratio, 2),
        "reason": "The independent verification path did not find sufficient support."
    }