def verify_claim(claim, evidence):

    if evidence["status"] == "NO_EVIDENCE":
        return {
            "status": "UNSUPPORTED",
            "confidence": 0.0,
            "reason": "No supporting evidence was found."
        }

    if evidence["status"] == "ERROR":
        return {
            "status": "NOT_VERIFIED",
            "confidence": 0.0,
            "reason": "Evidence retrieval failed."
        }

    sources = evidence.get("sources", [])

    if len(sources) == 0:
        return {
            "status": "UNSUPPORTED",
            "confidence": 0.0,
            "reason": "No sources were found."
        }

    # Combine evidence text
    evidence_text = " ".join(
        source.get("evidence", "")
        for source in sources
    ).lower()

    # Break claim into important words
    claim_words = [
        word.lower().strip(".,!?")
        for word in claim.split()
        if len(word) > 3
    ]

    if not claim_words:
        return {
            "status": "NOT_VERIFIED",
            "confidence": 0.0,
            "reason": "Claim could not be analyzed."
        }

    # Count how many important claim words appear in evidence
    matched_words = sum(
        1 for word in claim_words
        if word in evidence_text
    )

    match_ratio = matched_words / len(claim_words)

    if match_ratio >= 0.6:
        return {
            "status": "SUPPORTED",
            "confidence": round(
                min(0.95, 0.6 + match_ratio * 0.35),
                2
            ),
            "reason": "The retrieved evidence contains substantial information related to the claim."
        }

    if match_ratio >= 0.3:
        return {
            "status": "PARTIALLY_SUPPORTED",
            "confidence": round(
                match_ratio,
                2
            ),
            "reason": "The evidence is related to the claim but does not sufficiently support all of it."
        }

    return {
        "status": "UNSUPPORTED",
        "confidence": round(
            match_ratio,
            2
        ),
        "reason": "The retrieved evidence does not sufficiently support the claim."
    }