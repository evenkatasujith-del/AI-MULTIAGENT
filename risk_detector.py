def detect_risk(claim, verification, evidence=None):
    risks = []

    confidence = verification.get("confidence", 0)
    status = verification.get("status", "")

    # -----------------------------
    # 1. Confidence-based risks
    # -----------------------------
    if confidence < 0.5:
        risks.append("Low confidence")

    # -----------------------------
    # 2. Verification-status risks
    # -----------------------------
    if status == "UNSUPPORTED":
        risks.append("Unsupported claim")

    elif status == "PARTIALLY_SUPPORTED":
        risks.append("Insufficient supporting evidence")

    elif status == "NOT_VERIFIED":
        risks.append("Verification could not be completed")

    # -----------------------------
    # 3. Evidence-status risks
    # -----------------------------
    if evidence:
        evidence_status = evidence.get("status")

        if evidence_status == "NO_EVIDENCE":
            risks.append("No evidence found")

        elif evidence_status == "RATE_LIMIT":
            risks.append("Evidence retrieval was rate-limited")

        elif evidence_status == "ERROR":
            risks.append("Evidence retrieval failed")

    # -----------------------------
    # 4. Conservative contradiction check
    # -----------------------------
    #
    # IMPORTANT:
    # Do NOT use simple checks like:
    #
    # "is" in evidence
    #
    # because "is" also appears inside "is not".
    #
    # We only flag contradiction when the claim
    # and evidence contain a very similar phrase
    # with opposite negation.
    #

    if evidence and evidence.get("status") == "EVIDENCE_FOUND":

        claim_lower = claim.lower()

        for source in evidence.get("sources", []):
            evidence_text = source.get("evidence", "").lower()

            # Split into sentences so we compare
            # meaningful pieces rather than the whole page.
            sentences = [
                sentence.strip()
                for sentence in evidence_text.replace("!", ".").replace("?", ".").split(".")
                if sentence.strip()
            ]

            for sentence in sentences:

                # --------------------------------
                # Claim: "X is not Y"
                # Evidence: "X is Y"
                # --------------------------------
                if " is not " in claim_lower:
                    claim_parts = claim_lower.split(" is not ", 1)

                    if len(claim_parts) == 2:
                        subject = claim_parts[0].strip()
                        predicate = claim_parts[1].strip()

                        if (
                            subject
                            and predicate
                            and subject in sentence
                            and predicate in sentence
                            and " is not " not in sentence
                        ):
                            risks.append("Potential contradiction")

                # --------------------------------
                # Claim: "X does not Y"
                # Evidence: "X does Y"
                # --------------------------------
                if " does not " in claim_lower:
                    claim_parts = claim_lower.split(" does not ", 1)

                    if len(claim_parts) == 2:
                        subject = claim_parts[0].strip()
                        predicate = claim_parts[1].strip()

                        if (
                            subject
                            and predicate
                            and subject in sentence
                            and predicate in sentence
                            and " does not " not in sentence
                        ):
                            risks.append("Potential contradiction")

                # --------------------------------
                # Claim: "X cannot Y"
                # Evidence: "X can Y"
                # --------------------------------
                if " cannot " in claim_lower:
                    claim_parts = claim_lower.split(" cannot ", 1)

                    if len(claim_parts) == 2:
                        subject = claim_parts[0].strip()
                        predicate = claim_parts[1].strip()

                        if (
                            subject
                            and predicate
                            and subject in sentence
                            and predicate in sentence
                            and " cannot " not in sentence
                        ):
                            risks.append("Potential contradiction")

                # --------------------------------
                # Evidence says "X is not Y"
                # Claim says "X is Y"
                # --------------------------------
                if " is not " in sentence:
                    evidence_parts = sentence.split(" is not ", 1)

                    if len(evidence_parts) == 2:
                        subject = evidence_parts[0].strip()
                        predicate = evidence_parts[1].strip()

                        if (
                            subject
                            and predicate
                            and subject in claim_lower
                            and predicate in claim_lower
                            and " is not " not in claim_lower
                        ):
                            risks.append("Potential contradiction")

    # Remove duplicate risks
    risks = list(dict.fromkeys(risks))

    return {
        "risk_detected": len(risks) > 0,
        "risks": risks
    }