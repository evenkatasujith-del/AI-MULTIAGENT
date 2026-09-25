def get_evidence(claim):

    claim_lower = claim.lower()

    # Local evidence database for prototype testing
    evidence_database = [
        {
            "keywords": ["artificial intelligence", "field", "computer science"],
            "title": "Artificial Intelligence - Reference Evidence",
            "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "evidence": (
                "Artificial intelligence is a field of computer science "
                "concerned with creating systems capable of performing "
                "tasks that normally require human intelligence."
            )
        },
        {
            "keywords": ["ai", "computers", "tasks", "human intelligence"],
            "title": "Artificial Intelligence - Reference Evidence",
            "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "evidence": (
                "Artificial intelligence enables computer systems to perform "
                "tasks associated with human intelligence, including learning, "
                "reasoning, perception, and problem solving."
            )
        },
        {
            "keywords": ["ai", "healthcare", "transportation", "education"],
            "title": "Applications of Artificial Intelligence",
            "url": "https://en.wikipedia.org/wiki/Applications_of_artificial_intelligence",
            "evidence": (
                "Artificial intelligence has applications in healthcare, "
                "transportation, education, and many other fields."
            )
        }
    ]

    best_matches = []

    for item in evidence_database:

        matched = 0

        for keyword in item["keywords"]:
            if keyword in claim_lower:
                matched += 1

        if matched >= 2:
            best_matches.append(item)

    if not best_matches:

        return {
            "status": "NO_EVIDENCE",
            "sources": []
        }

    return {
        "status": "EVIDENCE_FOUND",
        "sources": best_matches
    }