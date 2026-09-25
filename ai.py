import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_answer(question):

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=question
    )

    return response.output_text


def extract_claims(answer):

    sentences = answer.replace("!", ".").replace("?", ".").split(".")

    claims = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) > 10:
            claims.append(sentence)

    return claims