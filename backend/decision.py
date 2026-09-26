def make_final_decision(
    verification,
    risk,
    correction,
    re_verification=None,
    independent_verification=None
):

    primary_status = verification.get("status", "UNSUPPORTED")
    primary_confidence = float(
        verification.get("confidence", 0.0)
    )

    independent_status = "NOT_VERIFIED"

    independent_confidence = 0.0

    if independent_verification:
        independent_status = independent_verification.get(
            "status",
            "NOT_VERIFIED"
        )

        independent_confidence = float(
            independent_verification.get(
                "confidence",
                0.0
            )
        )

    risk_detected = risk.get(
        "risk_detected",
        False
    )

    correction_action = correction.get(
        "action",
        "REJECT"
    )

    # -----------------------------------------
    # 1. REJECTED CLAIM
    # -----------------------------------------

    if correction_action == "REJECT":

        return {
            "status": "NOT_VERIFIED",
            "confidence": primary_confidence,
            "reason": (
                "The claim was rejected because "
                "there was insufficient supporting evidence."
            )
        }

    # -----------------------------------------
    # 2. RE-VERIFICATION
    # -----------------------------------------

    if re_verification:

        re_status = re_verification.get(
            "status",
            "NOT_VERIFIED"
        )

        re_confidence = float(
            re_verification.get(
                "confidence",
                0.0
            )
        )

        if re_status == "VERIFIED":

            return {
                "status": "VERIFIED_AFTER_CORRECTION",
                "confidence": re_confidence,
                "reason": (
                    "The corrected claim passed "
                    "re-verification."
                )
            }

    # -----------------------------------------
    # 3. HIGH-CONFIDENCE AGREEMENT
    # -----------------------------------------

    if (
        primary_status == "VERIFIED"
        and
        independent_status == "INDEPENDENTLY_SUPPORTED"
        and
        not risk_detected
    ):

        confidence = round(
            (primary_confidence +
             independent_confidence) / 2,
            2
        )

        return {
            "status": "VERIFIED",
            "confidence": confidence,
            "reason": (
                "The claim was strongly supported "
                "by primary and independent verification."
            )
        }

    # -----------------------------------------
    # 4. PRIMARY VERIFICATION STRONG
    # -----------------------------------------

    if (
        primary_status == "VERIFIED"
        and
        primary_confidence >= 0.70
        and
        not risk_detected
    ):

        return {
            "status": "VERIFIED",
            "confidence": primary_confidence,
            "reason": (
                "The claim received strong primary "
                "verification and no significant risk "
                "was detected."
            )
        }

    # -----------------------------------------
    # 5. INDEPENDENT SUPPORT
    # -----------------------------------------

    if (
        independent_status == "INDEPENDENTLY_SUPPORTED"
        and
        independent_confidence >= 0.65
        and
        not risk_detected
    ):

        return {
            "status": "VERIFIED",
            "confidence": independent_confidence,
            "reason": (
                "The claim received strong independent "
                "verification and no significant risk "
                "was detected."
            )
        }

    # -----------------------------------------
    # 6. PARTIAL VERIFICATION
    # -----------------------------------------

    if (
        primary_status == "PARTIALLY_VERIFIED"
        or
        independent_status == "INDEPENDENTLY_PARTIAL"
    ):

        confidence = max(
            primary_confidence,
            independent_confidence
        )

        return {
            "status": "PARTIALLY_VERIFIED",
            "confidence": confidence,
            "reason": (
                "The available evidence supports "
                "important parts of the claim, but "
                "does not fully verify every detail."
            )
        }

    # -----------------------------------------
    # 7. RISK DETECTED
    # -----------------------------------------

    if risk_detected:

        return {
            "status": "NOT_VERIFIED",
            "confidence": min(
                primary_confidence,
                independent_confidence
                if independent_confidence > 0
                else primary_confidence
            ),
            "reason": (
                "The claim could not be reliably "
                "verified because verification "
                "identified one or more risks."
            )
        }

    # -----------------------------------------
    # 8. DEFAULT
    # -----------------------------------------

    return {
        "status": "NOT_VERIFIED",
        "confidence": primary_confidence,
        "reason": (
            "The claim could not be reliably "
            "verified with the available evidence."
        )
    }