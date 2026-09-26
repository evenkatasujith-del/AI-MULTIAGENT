from evidence import get_evidence
from verifier import verify_claim


def reverify_claim(corrected_claim):

    evidence = get_evidence(corrected_claim)

    verification = verify_claim(
        corrected_claim,
        evidence
    )

    return {
        "claim": corrected_claim,
        "evidence": evidence,
        "verification": verification
    }