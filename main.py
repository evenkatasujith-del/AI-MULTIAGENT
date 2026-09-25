from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai import generate_answer, extract_claims
from evidence import get_evidence
from verifier import verify_claim
from independent_verifier import independent_verify
from risk_detector import detect_risk
from correction import correct_claim
from reverify import reverify_claim
from decision import make_final_decision


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

    answer = generate_answer(question)

    claims = extract_claims(answer)

    verified_claims = []

    for claim in claims:
        evidence = get_evidence(claim)

        verification = verify_claim(
            claim,
            evidence
        )

        independent_verification = independent_verify(
            claim,
            evidence
        )

        risk = detect_risk(
            claim,
            verification,
            evidence
        )

        correction = correct_claim(
            claim,
            risk
        )

        re_verification = None

        if correction["corrected"]:
            re_verification = reverify_claim(
                correction["corrected_claim"]
            )

        final_decision = make_final_decision(
            verification,
            risk,
            correction,
            re_verification
        )

        verified_claims.append({
            "claim": claim,
            "evidence": evidence,
            "verification": verification,
            "independent_verification": independent_verification,
            "risk": risk,
            "correction": correction,
            "re_verification": re_verification,
            "final_decision": final_decision
        })

    return {
        "status": "success",
        "question": question,
        "answer": answer,
        "claims": verified_claims
    }