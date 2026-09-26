import re


def detect_type(question):
    text = question.lower()

    # Coding keywords
    coding_keywords = [
        "write code",
        "give me code",
        "python code",
        "java code",
        "c code",
        "program",
        "implement",
        "function",
        "algorithm",
        "leetcode",
        "coding"
    ]

    if any(keyword in text for keyword in coding_keywords):
        return "CODE"

    # Math expressions / keywords
    math_keywords = [
        "calculate",
        "solve",
        "what is",
        "find the value",
        "equation",
        "multiply",
        "divide",
        "add",
        "subtract"
    ]

    # Detect obvious mathematical expressions
    if re.search(r"\d+\s*[\+\-\*\/]\s*\d+", text):
        return "MATH"

    if any(keyword in text for keyword in math_keywords):
        # Don't classify normal factual "what is..." questions as math
        if re.search(r"\d", text):
            return "MATH"

    return "FACT"