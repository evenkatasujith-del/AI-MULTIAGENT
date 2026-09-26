import re


# =========================================================
# TEXT HELPERS
# =========================================================

STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "and", "or", "of", "to", "in", "on", "for",
    "with", "that", "this", "these", "those",
    "can", "cannot", "could", "would", "should",
    "from", "as", "it", "its", "they", "their",
    "our", "we", "you", "than", "very", "just",
    "also", "some", "only", "not", "no",
    "have", "has", "had", "do", "does",
    "but", "so", "if", "even", "still",
    "into", "by", "through", "using", "used"
}


def normalize(text):
    text = text.lower()

    text = text.replace("–", " ")
    text = text.replace("—", " ")
    text = text.replace("-", " ")

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def get_words(text):
    return {
        word
        for word in re.findall(
            r"[a-zA-Z]+",
            normalize(text)
        )
        if len(word) > 2
        and word not in STOP_WORDS
    }


def get_source_text(source):
    title = source.get("title", "")
    evidence = source.get("evidence", "")

    return f"{title}. {evidence}"


# =========================================================
# CLAIM SPLITTING
# =========================================================

def split_claim(claim):
    """
    Keep most normal sentences together.

    Only split when the AI has clearly produced
    multiple independent sentences.
    """

    claim = claim.strip()

    # Split only on sentence boundaries.
    parts = re.split(
        r"(?<=[.!?])\s+",
        claim
    )

    parts = [
        part.strip(" .,;:")
        for part in parts
        if len(part.strip()) >= 20
    ]

    # If splitting created too many fragments,
    # treat the original claim as one claim.
    if len(parts) > 3:
        return [claim]

    return parts if parts else [claim]


# =========================================================
# TOPIC / CONCEPT SUPPORT
# =========================================================

CONCEPT_GROUPS = {

    "photosynthesis": [
        "photosynthesis",
        "chlorophyll",
        "light",
        "carbon dioxide",
        "water",
        "glucose",
        "oxygen",
        "calvin cycle",
    ],

    "machine_learning": [
        "machine learning",
        "algorithm",
        "model",
        "training",
        "data",
        "prediction",
        "learning",
    ],

    "artificial_intelligence": [
        "artificial intelligence",
        "machine learning",
        "reasoning",
        "learning",
        "decision",
    ],

    "computer_vision": [
        "computer vision",
        "image",
        "object",
        "face",
        "visual",
        "recognition",
    ],

    "speech_recognition": [
        "speech",
        "voice",
        "audio",
        "recognition",
    ],

    "robotics": [
        "robot",
        "robotics",
        "autonomous",
        "sensor",
    ],

    "database": [
        "database",
        "table",
        "query",
        "data",
        "record",
    ],

    "operating_system": [
        "operating system",
        "process",
        "memory",
        "kernel",
        "cpu",
    ],

    "underwater": [
        "underwater",
        "water",
        "gill",
        "gills",
        "lung",
        "lungs",
        "oxygen",
        "breathing",
    ],
}


def get_concepts(text):

    text = normalize(text)

    concepts = []

    for concept, terms in CONCEPT_GROUPS.items():

        if any(
            term in text
            for term in terms
        ):
            concepts.append(
                concept
            )

    return concepts


def concept_support(
    claim,
    evidence
):

    claim_concepts = get_concepts(
        claim
    )

    evidence_text = normalize(
        evidence
    )

    if not claim_concepts:
        return 0.0

    matched = 0

    for concept in claim_concepts:

        terms = CONCEPT_GROUPS[
            concept
        ]

        # Count concept as supported
        # if at least one strong term exists.
        if any(
            term in evidence_text
            for term in terms
        ):
            matched += 1

    return (
        matched / len(claim_concepts)
    )


# =========================================================
# WORD OVERLAP
# =========================================================

def calculate_overlap(
    claim,
    evidence
):

    claim_words = get_words(
        claim
    )

    evidence_words = get_words(
        evidence
    )

    if not claim_words:
        return 0.0

    matches = (
        claim_words
        .intersection(
            evidence_words
        )
    )

    return (
        len(matches)
        / len(claim_words)
    )


# =========================================================
# SPECIAL PHRASE SUPPORT
# =========================================================

def phrase_support(
    claim,
    evidence
):

    claim_text = normalize(
        claim
    )

    evidence_text = normalize(
        evidence
    )

    important_phrases = [

        "photosynthesis",
        "machine learning",
        "artificial intelligence",
        "computer vision",
        "speech recognition",
        "natural language processing",
        "calvin cycle",
        "light dependent reactions",
        "carbon dioxide",
        "dissolved oxygen",
        "operating system",
        "database",
        "neural network",
        "scuba diving",
    ]

    matches = 0

    for phrase in important_phrases:

        if phrase in claim_text:

            if phrase in evidence_text:
                matches += 1

    if matches == 0:
        return 0.0

    return min(
        matches * 0.25,
        1.0
    )


# =========================================================
# CONTRADICTION CHECK
# =========================================================

def has_contradiction(
    claim,
    evidence
):

    claim_text = normalize(
        claim
    )

    evidence_text = normalize(
        evidence
    )

    contradiction_pairs = [

        (
            "humans can breathe underwater",
            "drowning"
        ),

        (
            "humans breathe underwater",
            "drowning"
        ),

        (
            "extract oxygen from water",
            "extract oxygen from air"
        ),

        (
            "extract oxygen from water",
            "atmosphere"
        ),
    ]

    for claim_phrase, evidence_phrase in contradiction_pairs:

        if (
            claim_phrase in claim_text
            and evidence_phrase in evidence_text
        ):
            return True

    return False


# =========================================================
# EVALUATE ONE CLAIM
# =========================================================

def evaluate_claim(
    claim,
    sources
):

    best_score = 0.0
    best_source = None
    best_reason = ""

    for source in sources:

        title = source.get(
            "title",
            ""
        )

        evidence = source.get(
            "evidence",
            ""
        )

        relevance = float(
            source.get(
                "relevance",
                0.0
            )
        )

        source_text = (
            f"{title}. {evidence}"
        )

        overlap = calculate_overlap(
            claim,
            source_text
        )

        concepts = concept_support(
            claim,
            source_text
        )

        phrases = phrase_support(
            claim,
            source_text
        )

        contradiction = has_contradiction(
            claim,
            source_text
        )

        # -------------------------------------------------
        # Combined score
        # -------------------------------------------------

        score = (
            relevance * 0.40
            + overlap * 0.20
            + concepts * 0.20
            + phrases * 0.20
        )

        # Strong topical source can support
        # a claim even when wording differs.
        if relevance >= 0.55:
            score += 0.10

        if concepts >= 0.75:
            score += 0.10

        if contradiction:
            score *= 0.20

        score = min(
            score,
            1.0
        )

        if score > best_score:

            best_score = score
            best_source = title

            if contradiction:

                best_reason = (
                    "The evidence appears to "
                    "conflict with the claim."
                )

            elif score >= 0.70:

                best_reason = (
                    "Strong relevant evidence "
                    "supports the claim."
                )

            elif score >= 0.50:

                best_reason = (
                    "Relevant evidence provides "
                    "substantial support for the claim."
                )

            elif score >= 0.30:

                best_reason = (
                    "Some relevant evidence was found, "
                    "but support is incomplete."
                )

            else:

                best_reason = (
                    "The available evidence is weak."
                )

    return {
        "score": round(
            best_score,
            2
        ),
        "supporting_source": best_source,
        "reason": best_reason,
    }


# =========================================================
# MAIN VERIFICATION
# =========================================================

def verify_claim(
    claim,
    evidence
):

    print(
        "\n========== CLAIM VERIFICATION =========="
    )

    print(
        "CLAIM:",
        claim
    )

    # -----------------------------------------------------
    # No evidence
    # -----------------------------------------------------

    if not evidence:

        return {
            "status": "UNSUPPORTED",
            "confidence": 0.0,
            "reason": "No evidence was provided.",
            "supporting_source": None,
            "source_score": 0.0,
            "claim_parts": [],
        }

    sources = evidence.get(
        "sources",
        []
    )

    if not sources:

        return {
            "status": "UNSUPPORTED",
            "confidence": 0.0,
            "reason": (
                "No relevant evidence sources "
                "were retrieved."
            ),
            "supporting_source": None,
            "source_score": 0.0,
            "claim_parts": [],
        }

    # -----------------------------------------------------
    # Split claim only when necessary
    # -----------------------------------------------------

    claim_parts = split_claim(
        claim
    )

    print(
        "CLAIM PARTS:"
    )

    for index, part in enumerate(
        claim_parts,
        start=1
    ):

        print(
            f"{index}. {part}"
        )

    evaluations = []

    for part in claim_parts:

        result = evaluate_claim(
            part,
            sources
        )

        result["claim_part"] = part

        evaluations.append(
            result
        )

        print(
            "PART:",
            part
        )

        print(
            "SCORE:",
            result["score"]
        )

        print(
            "SOURCE:",
            result["supporting_source"]
        )

    # -----------------------------------------------------
    # Overall score
    # -----------------------------------------------------

    scores = [
        item["score"]
        for item in evaluations
    ]

    if not scores:

        confidence = 0.0

    else:

        confidence = (
            sum(scores)
            / len(scores)
        )

    confidence = round(
        confidence,
        2
    )

    # -----------------------------------------------------
    # Support levels
    # -----------------------------------------------------

    strong_parts = sum(
        1
        for score in scores
        if score >= 0.65
    )

    supported_parts = sum(
        1
        for score in scores
        if score >= 0.45
    )

    total_parts = len(
        scores
    )

    support_ratio = (
        supported_parts
        / total_parts
        if total_parts
        else 0
    )

    strong_ratio = (
        strong_parts
        / total_parts
        if total_parts
        else 0
    )

    # -----------------------------------------------------
    # Final status
    # -----------------------------------------------------

    if (
        total_parts > 0
        and strong_ratio >= 0.70
        and confidence >= 0.60
    ):

        status = "VERIFIED"

        reason = (
            "The retrieved evidence strongly "
            "supports the claim."
        )

    elif (
        total_parts > 0
        and support_ratio >= 0.50
        and confidence >= 0.40
    ):

        status = "PARTIALLY_VERIFIED"

        reason = (
            "The evidence supports important "
            "parts of the claim, but some "
            "details remain uncertain."
        )

    else:

        status = "UNSUPPORTED"

        reason = (
            "The available evidence does not "
            "provide sufficient support for the claim."
        )

    # -----------------------------------------------------
    # Best source
    # -----------------------------------------------------

    best = max(
        evaluations,
        key=lambda item: item["score"],
        default=None
    )

    supporting_source = (
        best["supporting_source"]
        if best
        else None
    )

    source_score = (
        best["score"]
        if best
        else 0.0
    )

    print(
        "FINAL VERIFICATION:",
        status
    )

    print(
        "CONFIDENCE:",
        confidence
    )

    print(
        "========================================\n"
    )

    return {
        "status": status,
        "confidence": confidence,
        "reason": reason,
        "supporting_source": supporting_source,
        "source_score": source_score,
        "claim_parts": evaluations,
    }