from reverify import reverify_claim
from correction import correct_claim
from risk_detector import detect_risk
from verifier import verify_claim
from ai import generate_answer, extract_claims
from evidence import get_evidence
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="VerifyAI")


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data we expect from the frontend
class QuestionRequest(BaseModel):
    question: str


# Home
@app.get("/")
def home():
    return {
        "message": "VerifyAI backend is running!"
    }


# Test
@app.get("/test")
def test():
    return {
        "status": "success",
        "message": "Backend is working correctly"
    }


# Verify endpoint
@app.post("/verify")
def verify(request: QuestionRequest):

    question = request.question

    answer = """
    Artificial intelligence is a field of computer science.
    AI allows computers to perform tasks that normally require human intelligence.
    AI is used in areas such as healthcare, transportation, and education.
    """

    claims = extract_claims(answer)

    verified_claims = []

  for claim in claims:

    # 1. Get evidence
    evidence = get_evidence(claim)

    # 2. Verify original claim
    verification = verify_claim(
        claim,
        evidence
    )

    # 3. Detect risks
    risk = detect_risk(
        claim,
        verification
    )

    # 4. Correct if necessary
    correction = correct_claim(
        claim,
        risk
    )

    # 5. Re-verify corrected claim if correction happened
    re_verification = None

    if correction["corrected"]:
        re_verification = reverify_claim(
            correction["corrected_claim"]
        )

    verified_claims.append({
        "claim": claim,
        "evidence": evidence,
        "verification": verification,
        "risk": risk,
        "correction": correction,
        "re_verification": re_verification
    })

    return {
        "status": "success",
        "question": question,
        "answer": answer,
        "claims": verified_claims
    }