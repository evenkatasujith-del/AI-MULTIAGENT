import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

print("Creating client...")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Starting Gemini...")

stream = client.interactions.create(
    model="gemini-3.8-flash",
    input="Say hello in one sentence.",
    stream=True
)

print("Receiving response:")

for event in stream:
    print(event)