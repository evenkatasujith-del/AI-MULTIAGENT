def detect_risk(claim, verification, evidence=None):

    risks = []

    # Low confidence
    if verification["confidence"] < 0.5:
        risks.append("Low confidence")

    # Unsupported claim
    if verification["status"] == "UNSUPPORTED":
        risks.append("Unsupported claim")

    # Partial support
    if verification["status"] == "PARTIALLY_SUPPORTED":
        risks.append("Insufficient supporting evidence")

    # Verification failure
    if verification["status"] == "NOT_VERIFIED":
        risks.append("Verification could not be completed")

    # No evidence
    if evidence and evidence.get("status") == "NO_EVIDENCE":
        risks.append("No evidence found")

    # Contradiction detection
    if evidence and evidence.get("status") == "EVIDENCE_FOUND":

        claim_lower = claim.lower()

        for source in evidence.get("sources", []):

            evidence_text = source.get("evidence", "").lower()

            # Simple contradiction patterns
            contradiction_pairs = [
                ("is not", "is"),
                ("was not", "was"),
                ("does not", "does"),
                ("cannot", "can"),
                ("never", "always")
            ]

            for negative, positive in contradiction_pairs:

                if negative in claim_lower and positive in evidence_text:
                    risks.append("Potential contradiction")

                elif positive in claim_lower and negative in evidence_text:
                    risks.append("Potential contradiction")

    # Remove duplicate risks
    risks = list(dict.fromkeys(risks))

    return {
        "risk_detected": len(risks) > 0,
        "risks": risks
    }