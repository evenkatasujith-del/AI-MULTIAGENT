import os
import re

from dotenv import load_dotenv
from groq import Groq

print("========== VERIFYAI USING NEW ai.py ==========")
print("🔥🔥🔥 NEW AI.PY LOADED 🔥🔥🔥")
# ============================================================
# GROQ SETUP
# ============================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)

MODEL = "openai/gpt-oss-20b"


# ============================================================
# GENERATOR AGENT
# ============================================================

def generate_answer(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are the Generator Agent of VerifyAI.

Answer the user's question clearly and accurately.

Rules:
1. Do not intentionally invent facts.
2. If something is uncertain, say so.
3. Keep the answer reasonably concise.
4. Use simple explanations.
5. You may use bullet points when useful.
6. Avoid unnecessary tables.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.2,
        include_reasoning=False
    )

    return response.choices[0].message.content


# ============================================================
# CLAIM EXTRACTION AGENT
# ============================================================

def extract_claims(answer):

    print("🔥🔥🔥 CLAIM EXTRACTION STARTED 🔥🔥🔥")

    prompt = f"""
You are the Claim Extraction Agent of VerifyAI.

Extract the important factual claims from the following AI answer.

Rules:
1. Return ONLY a JSON array of strings.
2. Each item must be a complete factual claim.
3. Do not return headings.
4. Do not return fragments such as "Light energy" or "Carbon dioxide".
5. Combine related fragments into one complete claim.
6. Keep each claim understandable without the original answer.
7. Do not add new information.
8. Extract at most 6 claims.
9. Ignore introductions, explanations, and formatting labels.

AI ANSWER:
{answer}

Example output:
[
  "Photosynthesis converts light energy into chemical energy.",
  "Plants use carbon dioxide and water to produce glucose.",
  "Oxygen is released as a byproduct."
]
"""

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise factual claim "
                        "extraction agent. Return valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            include_reasoning=False
        )

        result = response.choices[0].message.content.strip()

        print("RAW CLAIM EXTRACTION:")
        print(result)

        # Remove markdown code fences if the model adds them

        result = result.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

        import json

        claims = json.loads(result)

        if not isinstance(
            claims,
            list
        ):
            raise ValueError(
                "Claim extraction did not return a list."
            )

        cleaned_claims = []

        for claim in claims:

            if not isinstance(
                claim,
                str
            ):
                continue

            claim = re.sub(
                r"\s+",
                " ",
                claim
            ).strip()

            if len(claim) < 20:
                continue

            if claim not in cleaned_claims:

                cleaned_claims.append(
                    claim
                )

        cleaned_claims = cleaned_claims[:6]

        print("🔥🔥🔥 CLAIMS FOUND 🔥🔥🔥")

        for index, claim in enumerate(
            cleaned_claims,
            start=1
        ):

            print(
                f"{index}. {claim}"
            )

        print(
            "Total claims:",
            len(cleaned_claims)
        )

        print(
            "🔥🔥🔥 END CLAIM EXTRACTION 🔥🔥🔥"
        )

        return cleaned_claims

    except Exception as error:

        print(
            "Claim extraction error:",
            error
        )

        # Safe fallback

        return [
            answer.strip()
        ]
        
def generate_code(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are the Code Generation Agent of VerifyAI.

Generate a correct Python solution for the user's programming request.

Rules:
1. Return ONLY Python code.
2. Do not use markdown code fences.
3. Keep the solution simple.
4. Include example input directly in the code when necessary.
5. The code must be executable.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.1,
        include_reasoning=False
    )

    return response.choices[0].message.content.strip()