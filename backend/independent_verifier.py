import re


STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "and", "or", "of", "to", "in", "on", "for",
    "with", "that", "this", "these", "those",
    "can", "cannot", "could", "would", "should",
    "be", "by", "from", "as", "it", "its",
    "they", "their", "into", "over", "such",
    "which", "typically", "usually", "some",
    "using", "used", "use", "system", "systems",
    "task", "tasks", "able", "ability",
    "human", "humans"
}


def clean_words(text):
    words = re.findall(
        r"[a-zA-Z]+",
        text.lower()
    )

    return {
        word
        for word in words
        if len(word) > 2
        and word not in STOP_WORDS
    }


def calculate_keyword_overlap(claim, sentence):
    claim_words = clean_words(claim)
    sentence_words = clean_words(sentence)

    if not claim_words:
        return 0.0

    matches = claim_words.intersection(
        sentence_words
    )

    return len(matches) / len(claim_words)


def get_claim_concepts(claim):
    text = claim.lower()

    concepts = []

    concept_groups = {
        "underwater": [
            "underwater",
            "water",
            "breathe",
            "breathing",
            "lungs",
            "gills",
            "oxygen"
        ],

        "machine learning": [
            "machine learning",
            "training",
            "model",
            "data",
            "algorithm"
        ],

        "artificial intelligence": [
            "artificial intelligence",
            "ai",
            "reasoning",
            "learning",
            "decision"
        ],

        "photosynthesis": [
            "photosynthesis",
            "plant",
            "light",
            "chlorophyll",
            "carbon dioxide"
        ],

        "robotics": [
            "robot",
            "robotics",
            "autonomous"
        ],

        "database": [
            "database",
            "table",
            "query",
            "data"
        ],

        "operating system": [
            "operating system",
            "process",
            "memory",
            "kernel"
        ],

        "speech recognition": [
            "speech",
            "voice",
            "audio",
            "recognition"
        ],

        "computer vision": [
            "image",
            "vision",
            "object",
            "face",
            "visual"
        ],

        "natural language processing": [
            "language",
            "text",
            "translation",
            "linguistic",
            "nlp"
        ]
    }

    for concept, terms in concept_groups.items():

        if any(
            term in text
            for term in terms
        ):
            concepts.append(concept)

    return concepts


def concept_overlap(claim, evidence_sentence):
    claim_concepts = get_claim_concepts(
        claim
    )

    evidence_lower = (
        evidence_sentence.lower()
    )

    if not claim_concepts:
        return 0.0

    matched = 0

    for concept in claim_concepts:

        if concept in evidence_lower:
            matched += 1
            continue

        concept_terms = concept.split()

        if any(
            term in evidence_lower
            for term in concept_terms
        ):
            matched += 1

    return matched / len(
        claim_concepts
    )


def source_relevance_score(source):
    return float(
        source.get(
            "relevance",
            0
        )
    )


def split_into_sentences(text):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def score_sentence(
    claim,
    sentence,
    source
):

    keyword_score = (
        calculate_keyword_overlap(
            claim,
            sentence
        )
    )

    concept_score = (
        concept_overlap(
            claim,
            sentence
        )
    )

    source_score = (
        source_relevance_score(
            source
        )
    )

    # Balanced independent scoring
    score = (
        keyword_score * 0.45
        + concept_score * 0.30
        + source_score * 0.25
    )

    return round(
        min(score, 1.0),
        2
    )


def find_best_evidence(
    claim,
    sources
):

    best_result = None

    for source in sources:

        source_score = (
            source_relevance_score(
                source
            )
        )

        # Ignore extremely weak sources
        if source_score < 0.20:
            continue

        evidence = source.get(
            "evidence",
            ""
        )

        if not evidence:
            continue

        sentences = split_into_sentences(
            evidence
        )

        for sentence in sentences:

            score = score_sentence(
                claim,
                sentence,
                source
            )

            keyword_score = (
                calculate_keyword_overlap(
                    claim,
                    sentence
                )
            )

            concept_score = (
                concept_overlap(
                    claim,
                    sentence
                )
            )

            result = {
                "sentence": sentence,
                "score": score,
                "keyword_score": round(
                    keyword_score,
                    2
                ),
                "concept_score": round(
                    concept_score,
                    2
                ),
                "source_relevance": source_score,
                "source_title": source.get(
                    "title",
                    "Unknown source"
                )
            }

            if (
                best_result is None
                or score >
                best_result["score"]
            ):
                best_result = result

    return best_result


def independent_verify(
    claim,
    evidence
):

    print(
        "\n========== INDEPENDENT VERIFICATION =========="
    )

    print(
        "Claim:",
        claim
    )

    if evidence.get(
        "status"
    ) != "EVIDENCE_FOUND":

        print(
            "No usable evidence."
        )

        return {
            "status": "NOT_VERIFIED",
            "confidence": 0.0,
            "reason": (
                "Independent verification "
                "could not access usable evidence."
            )
        }

    sources = evidence.get(
        "sources",
        []
    )

    if not sources:

        return {
            "status": "NOT_VERIFIED",
            "confidence": 0.0,
            "reason": (
                "No evidence was available "
                "for independent verification."
            )
        }

    best_result = find_best_evidence(
        claim,
        sources
    )

    if best_result is None:

        return {
            "status": "NOT_VERIFIED",
            "confidence": 0.0,
            "reason": (
                "No sufficiently relevant "
                "evidence was found."
            )
        }

    score = best_result[
        "score"
    ]

    print(
        "Best source:",
        best_result[
            "source_title"
        ]
    )

    print(
        "Evidence score:",
        score
    )

    print(
        "Evidence sentence:",
        best_result[
            "sentence"
        ]
    )

    # Strong independent support
    if score >= 0.55:

        return {
            "status":
                "INDEPENDENTLY_SUPPORTED",

            "confidence":
                score,

            "reason": (
                "An independently selected "
                "evidence source provides "
                "strong support for the claim."
            ),

            "evidence_sentence":
                best_result[
                    "sentence"
                ],

            "supporting_source":
                best_result[
                    "source_title"
                ]
        }

    # Partial support
    if score >= 0.35:

        return {
            "status":
                "INDEPENDENTLY_PARTIAL",

            "confidence":
                score,

            "reason": (
                "Relevant evidence was found, "
                "but it does not provide "
                "strong enough support for "
                "the complete claim."
            ),

            "evidence_sentence":
                best_result[
                    "sentence"
                ],

            "supporting_source":
                best_result[
                    "source_title"
                ]
        }

    # Weak / unsupported
    return {
        "status":
            "NOT_VERIFIED",

        "confidence":
            score,

        "reason": (
            "The independent check did not "
            "find sufficiently strong evidence "
            "to support the claim."
        ),

        "evidence_sentence":
            best_result[
                "sentence"
            ],

        "supporting_source":
            best_result[
                "source_title"
            ]
    }