import re
import requests
from urllib.parse import quote


WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_REST = "https://en.wikipedia.org/api/rest_v1/page/summary/"

HEADERS = {
    "User-Agent": (
        "VerifyAI/1.0 "
        "(educational hackathon project; evidence retrieval system)"
    ),
    "Accept": "application/json",
}

MAX_SOURCES = 3
SEARCH_RESULTS_PER_TOPIC = 2
REQUEST_TIMEOUT = 8

PAGE_CACHE = {}


# =========================================================
# TOPIC MAP
# =========================================================

TOPIC_MAP = {

    "photosynthesis": [
        "Photosynthesis",
        "Chloroplast",
        "Chlorophyll",
        "Light-dependent reactions of photosynthesis",
        "Calvin cycle",
        "Food chain",
    ],

    "machine learning": [
        "Machine learning",
        "Artificial intelligence",
    ],

    "deep learning": [
        "Deep learning",
        "Artificial neural network",
    ],

    "neural network": [
        "Artificial neural network",
        "Deep learning",
    ],

    "artificial intelligence": [
        "Artificial intelligence",
        "Machine learning",
    ],

    "underwater breathing": [
        "Human respiratory system",
        "Lung",
        "Gill",
        "Drowning",
        "Scuba diving",
    ],

    "speech recognition": [
        "Speech recognition",
        "Automatic speech recognition",
    ],

    "computer vision": [
        "Computer vision",
        "Image processing",
    ],

    "natural language processing": [
        "Natural language processing",
        "Computational linguistics",
    ],

    "robotics": [
        "Robotics",
        "Robot",
    ],

    "database": [
        "Database",
        "Database management system",
    ],

    "operating system": [
        "Operating system",
    ],

    "computer science": [
        "Computer science",
    ],
}


# =========================================================
# TEXT HELPERS
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def word_set(text):

    words = re.findall(
        r"[a-zA-Z]+",
        text.lower()
    )

    return set(words)


def calculate_word_overlap(claim, evidence):

    claim_words = word_set(claim)
    evidence_words = word_set(evidence)

    if not claim_words:
        return 0.0

    matches = claim_words.intersection(
        evidence_words
    )

    return len(matches) / len(claim_words)


# =========================================================
# TOPIC DETECTION
# =========================================================

def detect_topics(claim):

    text = claim.lower()

    topics = []

    # -----------------------------------------------------
    # PHOTOSYNTHESIS
    # -----------------------------------------------------

    photosynthesis_signals = [

        "photosynthesis",

        "chlorophyll",

        "chloroplast",

        "calvin cycle",

        "light-dependent",

        "light dependent",

        "nadph",

        "atp",

        "carbon dioxide",

        "carbon dioxide and water",

        "water into glucose",

        "glucose and oxygen",

        "plants make food",

        "plants produce food",

        "plant food",

        "food chains",

        "food chain",

        "oxygen we breathe",

        "plants release oxygen",

        "plants produce oxygen",

        "light energy",
    ]

    if any(
        signal in text
        for signal in photosynthesis_signals
    ):

        topics.extend(
            TOPIC_MAP["photosynthesis"]
        )


    # -----------------------------------------------------
    # MACHINE LEARNING
    # -----------------------------------------------------

    if "machine learning" in text:

        topics.extend(
            TOPIC_MAP["machine learning"]
        )


    elif "deep learning" in text:

        topics.extend(
            TOPIC_MAP["deep learning"]
        )


    elif "neural network" in text:

        topics.extend(
            TOPIC_MAP["neural network"]
        )


    elif (
        "artificial intelligence" in text
        or text.startswith("ai ")
    ):

        topics.extend(
            TOPIC_MAP["artificial intelligence"]
        )


    # -----------------------------------------------------
    # UNDERWATER BREATHING
    # -----------------------------------------------------
    # IMPORTANT:
    # Do NOT trigger this just because "breathe"
    # or "oxygen" appears.
    # -----------------------------------------------------

    underwater_signal = (
        "underwater" in text
        and any(
            word in text
            for word in [
                "breathe",
                "breathing",
                "breath",
                "lungs",
                "gills",
            ]
        )
    )

    explicit_underwater_signal = (
        "breathe underwater" in text
        or "breathing underwater" in text
    )

    if (
        underwater_signal
        or explicit_underwater_signal
    ):

        topics.extend(
            TOPIC_MAP["underwater breathing"]
        )


    # -----------------------------------------------------
    # SPEECH RECOGNITION
    # -----------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "speech recognition",
            "speech to text",
            "voice recognition",
        ]
    ):

        topics.extend(
            TOPIC_MAP["speech recognition"]
        )


    # -----------------------------------------------------
    # COMPUTER VISION
    # -----------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "computer vision",
            "image recognition",
            "object detection",
            "face recognition",
        ]
    ):

        topics.extend(
            TOPIC_MAP["computer vision"]
        )


    # -----------------------------------------------------
    # NLP
    # -----------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "natural language processing",
            "nlp",
        ]
    ):

        topics.extend(
            TOPIC_MAP["natural language processing"]
        )


    # -----------------------------------------------------
    # ROBOTICS
    # -----------------------------------------------------

    if (
        "robot" in text
        or "robotics" in text
    ):

        topics.extend(
            TOPIC_MAP["robotics"]
        )


    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------

    if (
        "database" in text
        or "dbms" in text
    ):

        topics.extend(
            TOPIC_MAP["database"]
        )


    # -----------------------------------------------------
    # OPERATING SYSTEM
    # -----------------------------------------------------

    if "operating system" in text:

        topics.extend(
            TOPIC_MAP["operating system"]
        )


    # -----------------------------------------------------
    # COMPUTER SCIENCE
    # -----------------------------------------------------

    if "computer science" in text:

        topics.extend(
            TOPIC_MAP["computer science"]
        )


    # Remove duplicates

    return list(
        dict.fromkeys(topics)
    )


# =========================================================
# SEARCH QUERY
# =========================================================

def build_search_query(claim):

    text = claim.lower()


    # -----------------------------------------------------
    # PHOTOSYNTHESIS
    # -----------------------------------------------------

    photosynthesis_signals = [

        "photosynthesis",
        "chlorophyll",
        "chloroplast",
        "calvin cycle",
        "food chain",
        "food chains",
        "oxygen we breathe",
        "plants make food",
        "plants produce food",
        "plants release oxygen",
        "light energy",
        "carbon dioxide",
        "glucose",
    ]

    if any(
        signal in text
        for signal in photosynthesis_signals
    ):

        return (
            "photosynthesis plants "
            "chloroplast chlorophyll "
            "light carbon dioxide water "
            "glucose oxygen food chain"
        )


    # -----------------------------------------------------
    # MACHINE LEARNING
    # -----------------------------------------------------

    if "machine learning" in text:

        return (
            "machine learning "
            "algorithms data models training"
        )


    # -----------------------------------------------------
    # DEEP LEARNING
    # -----------------------------------------------------

    if "deep learning" in text:

        return (
            "deep learning "
            "neural networks machine learning"
        )


    # -----------------------------------------------------
    # NEURAL NETWORK
    # -----------------------------------------------------

    if "neural network" in text:

        return (
            "artificial neural network "
            "machine learning"
        )


    # -----------------------------------------------------
    # ARTIFICIAL INTELLIGENCE
    # -----------------------------------------------------

    if "artificial intelligence" in text:

        return (
            "artificial intelligence "
            "machine learning"
        )


    # -----------------------------------------------------
    # UNDERWATER
    # -----------------------------------------------------

    if (
        "breathe underwater" in text
        or "breathing underwater" in text
    ):

        return (
            "human breathing underwater "
            "lungs gills oxygen"
        )


    # -----------------------------------------------------
    # SPEECH
    # -----------------------------------------------------

    if "speech recognition" in text:

        return (
            "speech recognition "
            "speech to text"
        )


    # -----------------------------------------------------
    # COMPUTER VISION
    # -----------------------------------------------------

    if "computer vision" in text:

        return (
            "computer vision "
            "image recognition"
        )


    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------

    if "database" in text:

        return (
            "database "
            "database management system"
        )


    # -----------------------------------------------------
    # OPERATING SYSTEM
    # -----------------------------------------------------

    if "operating system" in text:

        return (
            "operating system "
            "process memory kernel"
        )


    # -----------------------------------------------------
    # GENERIC SEARCH
    # -----------------------------------------------------

    words = re.findall(
        r"[a-zA-Z]+",
        text
    )

    words = [
        word
        for word in words
        if len(word) > 3
    ]

    words = words[:10]

    return " ".join(words)


# =========================================================
# WIKIPEDIA SEARCH
# =========================================================

def wikipedia_search(query):

    params = {

        "action": "query",

        "format": "json",

        "list": "search",

        "srsearch": query,

        "srlimit": SEARCH_RESULTS_PER_TOPIC,

        "srnamespace": 0,
    }

    try:

        response = requests.get(
            WIKIPEDIA_API,
            params=params,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "query",
            {}
        ).get(
            "search",
            []
        )

        return results

    except Exception as error:

        print(
            "Wikipedia search error:",
            error
        )

        return []


# =========================================================
# PAGE EXTRACT
# =========================================================

def get_page_extract(title):

    if title in PAGE_CACHE:

        return PAGE_CACHE[title]


    url = (
        WIKIPEDIA_REST
        + quote(title)
    )

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        extract = clean_text(
            data.get(
                "extract",
                ""
            )
        )

        PAGE_CACHE[title] = extract

        return extract

    except Exception as error:

        print(
            "Wikipedia page error:",
            error
        )

        return ""


# =========================================================
# BAD TITLES
# =========================================================

def is_bad_title(title):

    if not title:

        return True

    bad_words = [

        "disambiguation",

        "list of",

        "index of",

    ]

    title_lower = title.lower()

    return any(
        word in title_lower
        for word in bad_words
    )


# =========================================================
# CONCEPT SCORE
# =========================================================

def concept_score(claim, title, evidence):

    claim_text = claim.lower()

    title_text = title.lower()

    combined = (
        title_text
        + " "
        + evidence.lower()
    )

    score = 0.0


    # -----------------------------------------------------
    # PHOTOSYNTHESIS
    # -----------------------------------------------------

    photosynthesis_signals = [

        "photosynthesis",
        "chlorophyll",
        "chloroplast",
        "calvin cycle",
        "food chain",
        "food chains",
        "glucose",
        "oxygen",
        "carbon dioxide",
        "light energy",
    ]

    claim_has_photosynthesis = any(
        signal in claim_text
        for signal in photosynthesis_signals
    )

    if claim_has_photosynthesis:

        if "photosynthesis" in title_text:
            score += 0.45

        if "chloroplast" in combined:
            score += 0.10

        if "chlorophyll" in combined:
            score += 0.10

        if "light" in combined:
            score += 0.08

        if "carbon dioxide" in combined:
            score += 0.08

        if "water" in combined:
            score += 0.05

        if "oxygen" in combined:
            score += 0.05

        if "glucose" in combined:
            score += 0.05

        if (
            "food chain" in claim_text
            or "food chains" in claim_text
        ):

            if "food chain" in combined:

                score += 0.30


    # -----------------------------------------------------
    # MACHINE LEARNING
    # -----------------------------------------------------

    if "machine learning" in claim_text:

        if "machine learning" in combined:

            score += 0.50

        if "algorithm" in combined:

            score += 0.15

        if "training" in combined:

            score += 0.15


    # -----------------------------------------------------
    # ARTIFICIAL INTELLIGENCE
    # -----------------------------------------------------

    if "artificial intelligence" in claim_text:

        if "artificial intelligence" in combined:

            score += 0.50

        if "machine learning" in combined:

            score += 0.20


    # -----------------------------------------------------
    # ROBOTICS
    # -----------------------------------------------------

    if (
        "robot" in claim_text
        or "robotics" in claim_text
    ):

        if "robot" in combined:

            score += 0.50

        if "autonomous" in combined:

            score += 0.15


    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------

    if (
        "database" in claim_text
        or "dbms" in claim_text
    ):

        if "database" in combined:

            score += 0.50

        if "query" in combined:

            score += 0.15


    # -----------------------------------------------------
    # OPERATING SYSTEM
    # -----------------------------------------------------

    if "operating system" in claim_text:

        if "operating system" in combined:

            score += 0.50

        if "kernel" in combined:

            score += 0.15

        if "process" in combined:

            score += 0.10


    return min(
        score,
        1.0
    )


# =========================================================
# RELEVANCE
# =========================================================

def calculate_relevance(
    claim,
    title,
    evidence
):

    overlap = calculate_word_overlap(
        claim,
        evidence
    )

    concept = concept_score(
        claim,
        title,
        evidence
    )

    title_words = word_set(title)

    claim_words = word_set(claim)

    title_match = 0.0

    if title_words:

        title_match = len(
            title_words.intersection(
                claim_words
            )
        ) / len(title_words)


    score = (
        overlap * 0.20
        + concept * 0.65
        + title_match * 0.15
    )

    return round(
        min(score, 1.0),
        2
    )


# =========================================================
# USEFUL SOURCE
# =========================================================

def is_useful_source(
    claim,
    title,
    evidence
):

    if not evidence:

        return False

    if is_bad_title(title):

        return False

    relevance = calculate_relevance(
        claim,
        title,
        evidence
    )

    return relevance >= 0.30


# =========================================================
# FETCH SOURCES
# =========================================================

def fetch_sources(
    claim,
    topics
):

    sources = []


    # First search topic pages

    for topic in topics:

        results = wikipedia_search(
            topic
        )

        for result in results:

            title = result.get(
                "title",
                ""
            )

            if is_bad_title(title):

                continue

            evidence = get_page_extract(
                title
            )

            if not evidence:

                continue

            if not is_useful_source(
                claim,
                title,
                evidence
            ):

                continue

            relevance = calculate_relevance(
                claim,
                title,
                evidence
            )

            sources.append({

                "title": title,

                "evidence": evidence,

                "relevance": relevance,

                "url": (
                    "https://en.wikipedia.org/wiki/"
                    + quote(
                        title.replace(
                            " ",
                            "_"
                        )
                    )
                )

            })


    # If no good topic source exists,
    # perform direct claim search.

    if not sources:

        query = build_search_query(
            claim
        )

        print(
            "DIRECT SEARCH QUERY:",
            query
        )

        results = wikipedia_search(
            query
        )

        for result in results:

            title = result.get(
                "title",
                ""
            )

            if is_bad_title(title):

                continue

            evidence = get_page_extract(
                title
            )

            if not evidence:

                continue

            if not is_useful_source(
                claim,
                title,
                evidence
            ):

                continue

            relevance = calculate_relevance(
                claim,
                title,
                evidence
            )

            sources.append({

                "title": title,

                "evidence": evidence,

                "relevance": relevance,

                "url": 
                    "https://en.wikipedia.org/wiki/"
                    + quote(
                        title.replace(
                            " ",
                            "_"
                        )
                    )
                })

    return sources


# =========================================================
# DEDUPLICATE
# =========================================================

def deduplicate_sources(
    sources
):

    unique = {}

    for source in sources:

        title = source.get(
            "title",
            ""
        )

        if title not in unique:

            unique[title] = source

        else:

            if (
                source.get(
                    "relevance",
                    0
                )
                >
                unique[title].get(
                    "relevance",
                    0
                )
            ):

                unique[title] = source


    sources = list(
        unique.values()
    )

    sources.sort(
        key=lambda x: x.get(
            "relevance",
            0
        ),
        reverse=True
    )

    return sources[
        :MAX_SOURCES
    ]


# =========================================================
# MAIN EVIDENCE FUNCTION
# =========================================================

def get_evidence(claim):

    print("\n========== EVIDENCE RETRIEVAL ==========")

    print(
        "Claim:",
        claim
    )


    topics = detect_topics(
        claim
    )

    print(
        "TOPICS:",
        topics
    )


    sources = fetch_sources(
        claim,
        topics
    )

    sources = deduplicate_sources(
        sources
    )


    if not sources:

        print(
            "NO_EVIDENCE"
        )

        return {

            "status": "NO_EVIDENCE",

            "claim": claim,

            "sources": [],

            "message": (
                "Insufficient evidence was found "
                "to reliably verify this claim."
            )
        }


    print(
        "SOURCES FOUND:",
        len(sources)
    )


    for index, source in enumerate(
        sources,
        start=1
    ):

        print(
            f"{index}. "
            f"{source['title']} "
            f"({source['relevance']})"
        )


    return {

        "status": "EVIDENCE_FOUND",

        "claim": claim,

        "sources": sources
    }