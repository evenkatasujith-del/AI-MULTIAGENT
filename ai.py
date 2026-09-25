import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def generate_answer(question):

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=f"""
You are the Generator Agent of VerifyAI.

Answer the user's question clearly and accurately.

User question:
{question}
"""
    )

    return interaction.output_text

def extract_claims(answer):

    lines = answer.splitlines()
    claims = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("---"):
            continue

        if line.startswith("#"):
            continue

        line = line.lstrip("*- ")

        line = re.sub(r"^\d+\.\s*", "", line)

        if len(line) < 20:
            continue

        line = line.replace("**", "")

        claims.append(line.strip())

    return claims