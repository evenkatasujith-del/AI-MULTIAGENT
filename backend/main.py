import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai import generate_answer, extract_claims, generate_code
from evidence import get_evidence
from verifier import verify_claim
from independent_verifier import independent_verify
from risk_detector import detect_risk
from correction import correct_claim
from reverify import reverify_claim
from decision import make_final_decision
from math_verifier import verify_math
from code_sandbox import run_code
from router import detect_type
from multi_agent_verifier import (
    verify_claim_dual_agents,
    verify_math_dual_agents,
    verify_code_dual_agents,
)


app = FastAPI(title="VerifyAI")


# ========================================
# CORS
# ========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# REQUEST MODELS
# ========================================

class QuestionRequest(BaseModel):
    question: str
    response: str | None = None
    ai_response: str | None = None
    gemini_api_key: str | None = None


class MathRequest(BaseModel):
    expression: str
    expected_answer: float


class CodeRequest(BaseModel):
    code: str


# ========================================
# HOME
# ========================================

@app.get("/")
def home():
    return {
        "message": "VerifyAI backend is running!"
    }


# ========================================
# TEST
# ========================================

@app.get("/test")
def test():
    return {
        "status": "success",
        "message": "Backend is working correctly"
    }


# ========================================
# FACT VERIFICATION
# ========================================

@app.post("/verify")
def verify(request: QuestionRequest):

    question = request.question
    user_response = (request.response or request.ai_response or "").strip()
    is_user_response = bool(user_response)

    print("\n========================================")
    print("VERIFYAI STARTED")
    print("Question:", question)
    print("Provided response:", "YES (" + str(len(user_response)) + " chars)" if is_user_response else "NO (Auto-generate)")
    print("========================================\n")

    # Generate answer or use provided response
    if is_user_response:
        answer = user_response
        print("========== USING PROVIDED ANSWER ==========")
        print(answer)
        print("===========================================\n")
    else:
        answer = generate_answer(question)
        print("========== GENERATED ANSWER ==========")
        print(answer)
        print("======================================\n")

    # Extract claims
    claims = extract_claims(answer)

    print("========== CLAIMS ==========")

    for index, claim in enumerate(claims, start=1):
        print(f"{index}. {claim}")

    print("Total claims:", len(claims))
    print("============================\n")

    verified_claims = []

    # Verify every claim
    for index, claim in enumerate(claims, start=1):

        print("----------------------------------------")
        print(f"PROCESSING CLAIM {index}")
        print(claim)
        print("----------------------------------------")

        # Evidence retrieval
        evidence = get_evidence(claim)

        print("Evidence status:", evidence.get("status"))

        # Primary verification
        verification = verify_claim(
            claim,
            evidence
        )

        print("Primary verification:")
        print(verification)

        # Independent verification
        independent_verification = independent_verify(
            claim,
            evidence
        )

        print("Independent verification:")
        print(independent_verification)

        # Risk detection
        risk = detect_risk(
            claim,
            verification,
            evidence
        )

        print("Risk:")
        print(risk)

        # Correction
        correction = correct_claim(
            claim,
            risk
        )

        print("Correction:")
        print(correction)

        # Re-verification
        re_verification = None

        if (
            correction.get("corrected")
            and correction.get("corrected_claim")
            and correction.get("action") == "QUALIFY"
        ):

            re_verification = reverify_claim(
                correction["corrected_claim"]
            )

            print("Re-verification:")
            print(re_verification)

        # Final decision
        final_decision = make_final_decision(
            verification,
            risk,
            correction,
            re_verification,
            independent_verification
        )

        print("Final decision:")
        print(final_decision)

        # Store result
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

    print("\n========================================")
    print("VERIFYAI FINISHED")
    print("Verified claims:", len(verified_claims))
    print("========================================\n")

    return {
        "status": "success",
        "type": "FACT",
        "question": question,
        "answer": answer,
        "pasted_response": user_response if is_user_response else None,
        "is_user_response": is_user_response,
        "claims": verified_claims
    }


# ========================================
# MATH VERIFICATION
# ========================================

@app.post("/verify-math")
def verify_math_endpoint(request: MathRequest):

    result = verify_math(
        request.expression,
        request.expected_answer
    )

    return {
        "status": "success",
        "type": "MATH",
        "expression": request.expression,
        "result": result
    }


# ========================================
# CODE VERIFICATION
# ========================================

@app.post("/verify-code")
def verify_code_endpoint(request: CodeRequest):

    result = run_code(
        request.code
    )

    return {
        "status": "success",
        "type": "CODE",
        "result": result
    }


def extract_code_snippet(raw: str) -> str:
    import re
    cleaned = raw.strip()
    match = re.search(r"```(?:python)?\s*[\r\n]+(.*?)\s*```", cleaned, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned[3:-3].strip()
        if cleaned.lower().startswith("python"):
            cleaned = cleaned[6:].strip()
        return cleaned.strip()
    match_single = re.search(r"^`+(?:python)?\s*[\r\n]+(.*?)\s*`+$", cleaned, re.DOTALL | re.IGNORECASE)
    if match_single:
        return match_single.group(1).strip()
    return cleaned


# ========================================
# GENERATE + VERIFY CODE
# ========================================

@app.post("/generate-and-verify-code")
def generate_and_verify_code(request: QuestionRequest):

    question = request.question
    user_response = (request.response or request.ai_response or "").strip()
    is_user_response = bool(user_response)

    print("\n========== CODE VERIFICATION ==========")
    print("Question:", question)
    print("Provided response:", "YES" if is_user_response else "NO (Auto-generate)")

    if is_user_response:
        code = extract_code_snippet(user_response)
        print("\nUsing pasted code:")
    else:
        # Generate code
        code = generate_code(question)
        print("\nGenerated code:")

    print(code)

    # Execute code
    execution = run_code(code)

    print("\nExecution result:")
    print(execution)

    return {
        "status": "success",
        "type": "CODE",
        "question": question,
        "generated_code": code,
        "pasted_response": user_response if is_user_response else None,
        "is_user_response": is_user_response,
        "execution": execution
    }


# ========================================
# SMART VERIFY
# ========================================

@app.post("/smart-verify")
def smart_verify(request: QuestionRequest):

    question = request.question
    user_response = (request.response or request.ai_response or "").strip()
    is_user_response = bool(user_response)

    # Detect question type
    question_type = detect_type(question)

    print("\n========================================")
    print("SMART VERIFY")
    print("Question:", question)
    print("Detected type:", question_type)
    print("Provided AI response:", "YES (" + str(len(user_response)) + " chars)" if is_user_response else "NO (Auto-generate)")
    print("========================================\n")


    gemini_key = request.gemini_api_key

    # ====================================
    # CODE
    # ====================================

    if question_type == "CODE":

        print("========== CODE PATH ==========")

        if is_user_response:
            code = extract_code_snippet(user_response)
            print("Using pasted code:")
        else:
            # Generate code
            code = generate_code(question)
            print("Generated code:")

        print(code)

        # Run code in sandbox
        execution = run_code(code)

        print("Execution:")
        print(execution)

        # Dual Agent Code Verification (Groq + Gemini)
        multi_agent_res = verify_code_dual_agents(question, code, gemini_key)
        print("Multi-Agent Code Review:", multi_agent_res.get("consensus_confidence"), multi_agent_res.get("latency"))

        # If code failed, try correction
        correction = None
        corrected_execution = None

        if not execution.get("success"):

            print("Code execution failed.")

            correction = {
                "status": "FAILED",
                "message": "Pasted code failed during sandbox execution." if is_user_response else "Generated code failed during sandbox execution."
            }

        return {
            "status": "success",
            "type": "CODE",
            "question": question,
            "generated_code": code,
            "pasted_response": user_response if is_user_response else None,
            "is_user_response": is_user_response,
            "execution": execution,
            "correction": correction,
            "corrected_execution": corrected_execution,
            "multi_agent": multi_agent_res,
            "confidence": multi_agent_res.get("consensus_confidence", 0.95),
            "latency": multi_agent_res.get("latency", {})
        }


    # ====================================
    # MATH
    # ====================================

    elif question_type == "MATH":

        print("========== MATH PATH ==========")

        if is_user_response:
            answer = user_response
            print("Using pasted math answer:")
        else:
            # Generate AI answer
            answer = generate_answer(question)
            print("AI math answer:")

        print(answer)

        from math_verifier import verify_math_solution
        math_result = verify_math_solution(question, answer)

        print("Math verification:")
        print(math_result)

        # Dual Agent Math Verification (Groq + Gemini)
        multi_agent_res = verify_math_dual_agents(question, answer, gemini_key)
        print("Multi-Agent Math Review:", multi_agent_res.get("consensus_confidence"), multi_agent_res.get("latency"))

        final_val = math_result.get("final_answer") or math_result.get("calculated")
        if final_val is None:
            final_val = math_result.get("expected")

        return {
            "status": "success",
            "type": "MATH",
            "question": question,
            "answer": answer,
            "pasted_response": user_response if is_user_response else None,
            "is_user_response": is_user_response,
            "ai_answer": final_val if final_val is not None else answer,
            "expression": math_result.get("expression", ""),
            "verification": math_result,
            "multi_agent": multi_agent_res,
            "confidence": multi_agent_res.get("consensus_confidence", 0.95),
            "latency": multi_agent_res.get("latency", {})
        }


    # ====================================
    # FACT
    # ====================================

    else:

        print("========== FACT PATH ==========")

        if is_user_response:
            answer = user_response
            print("Using pasted answer:")
        else:
            # Generate answer
            answer = generate_answer(question)
            print("Generated answer:")

        print(answer)

        # Extract claims
        claims = extract_claims(answer)

        verified_claims = []

        # Verify each claim
        for index, claim in enumerate(claims, start=1):

            print("----------------------------------------")
            print(f"PROCESSING CLAIM {index}")
            print(claim)
            print("----------------------------------------")

            # Evidence
            evidence = get_evidence(claim)

            # Primary verification
            verification = verify_claim(
                claim,
                evidence
            )

            # Independent verification
            independent_verification = independent_verify(
                claim,
                evidence
            )

            # Risk detection
            risk = detect_risk(
                claim,
                verification,
                evidence
            )

            # Correction
            correction = correct_claim(
                claim,
                risk
            )

            # Re-verification
            re_verification = None

            if (
                correction.get("corrected")
                and correction.get("corrected_claim")
                and correction.get("action") == "QUALIFY"
            ):

                re_verification = reverify_claim(
                    correction["corrected_claim"]
                )

            # Final decision
            final_decision = make_final_decision(
                verification,
                risk,
                correction,
                re_verification,
                independent_verification
            )

            # Dual AI Agents Verification (Groq + Gemini)
            dual_agents = verify_claim_dual_agents(question, claim, gemini_key)
            print(f"Dual Agents (Claim {index}): Consensus={dual_agents.get('consensus_verdict')}, Conf={dual_agents.get('consensus_confidence')}, Latency={dual_agents.get('latency')}")

            verified_claims.append({
                "claim": claim,
                "evidence": evidence,
                "verification": verification,
                "independent_verification": independent_verification,
                "risk": risk,
                "correction": correction,
                "re_verification": re_verification,
                "final_decision": final_decision,
                "dual_agents": dual_agents,
                "confidence": dual_agents.get("consensus_confidence", 0.9),
                "latency": dual_agents.get("latency", {})
            })

        total_groq_ms = round(sum(c.get("dual_agents", {}).get("latency", {}).get("groq_ms", 0.0) for c in verified_claims), 1)
        total_gemini_ms = round(sum(c.get("dual_agents", {}).get("latency", {}).get("gemini_ms", 0.0) for c in verified_claims), 1)
        total_wall_ms = round(sum(c.get("dual_agents", {}).get("latency", {}).get("total_ms", 0.0) for c in verified_claims), 1)
        avg_confidence = round(sum(c.get("confidence", 0.9) for c in verified_claims) / len(verified_claims), 2) if verified_claims else 0.9

        return {
            "status": "success",
            "type": "FACT",
            "question": question,
            "answer": answer,
            "pasted_response": user_response if is_user_response else None,
            "is_user_response": is_user_response,
            "claims": verified_claims,
            "confidence": avg_confidence,
            "latency": {
                "groq_ms": total_groq_ms,
                "gemini_ms": total_gemini_ms,
                "total_ms": total_wall_ms
            },
            "multi_agent": {
                "groq_total_ms": total_groq_ms,
                "gemini_total_ms": total_gemini_ms,
                "total_ms": total_wall_ms,
                "gemini_status": verified_claims[0]["dual_agents"]["agents"]["gemini"]["status"] if verified_claims else "unknown"
            }
        }