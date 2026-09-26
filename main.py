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

    print("\n========================================")
    print("VERIFYAI STARTED")
    print("Question:", question)
    print("========================================\n")

    # Generate answer
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


# ========================================
# GENERATE + VERIFY CODE
# ========================================

@app.post("/generate-and-verify-code")
def generate_and_verify_code(request: QuestionRequest):

    question = request.question

    print("\n========== CODE VERIFICATION ==========")
    print("Question:", question)

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
        "execution": execution
    }


# ========================================
# SMART VERIFY
# ========================================

@app.post("/smart-verify")
def smart_verify(request: QuestionRequest):

    question = request.question

    # Detect question type
    question_type = detect_type(question)

    print("\n========================================")
    print("SMART VERIFY")
    print("Question:", question)
    print("Detected type:", question_type)
    print("========================================\n")


    # ====================================
    # CODE
    # ====================================

    if question_type == "CODE":

        print("========== CODE PATH ==========")

        # Generate code
        code = generate_code(question)

        print("Generated code:")
        print(code)

        # Run generated code
        execution = run_code(code)

        print("Execution:")
        print(execution)

        # If code failed, try correction
        correction = None
        corrected_execution = None

        if not execution.get("success"):

            print("Code execution failed.")

            correction = {
                "status": "FAILED",
                "message": "Generated code failed during sandbox execution."
            }

        return {
            "status": "success",
            "type": "CODE",
            "question": question,
            "generated_code": code,
            "execution": execution,
            "correction": correction,
            "corrected_execution": corrected_execution
        }


    # ====================================
    # MATH
    # ====================================

    elif question_type == "MATH":

        print("========== MATH PATH ==========")

        # Generate AI answer
        answer = generate_answer(question)

        print("AI math answer:")
        print(answer)

        import re

        # Find numbers in AI answer
        numbers = re.findall(
            r"-?\d+(?:\.\d+)?",
            answer
        )

        if numbers:

            ai_answer = float(numbers[-1])

            # Find simple mathematical expression
            expression_match = re.search(
                r"\d+(?:\s*[\+\-\*\/]\s*\d+)+",
                question
            )

            if expression_match:

                expression = expression_match.group()

                print("Expression:", expression)
                print("AI answer:", ai_answer)

                # Independent calculation
                math_result = verify_math(
                    expression,
                    ai_answer
                )
        if math_result["verified"]:

            return {
        "status": "success",
        "type": "MATH",
        "question": question,
        "ai_answer": ai_answer,
        "expression": expression,
        "verification": math_result,
        "final_answer": math_result["calculated"],
        "corrected": False
    }

        else:

                return {
        "status": "success",
        "type": "MATH",
        "question": question,
        "ai_answer": ai_answer,
        "expression": expression,
        "verification": math_result,
        "final_answer": math_result["calculated"],
        "corrected": True
    }

                print("Math verification:")
                print(math_result)

                return {
                    "status": "success",
                    "type": "MATH",
                    "question": question,
                    "ai_answer": ai_answer,
                    "expression": expression,
                    "verification": math_result
                }

        # If expression could not be extracted
        return {
            "status": "success",
            "type": "MATH",
            "question": question,
            "answer": answer,
            "verification": {
                "status": "NOT_VERIFIED",
                "verified": False,
                "reason": (
                    "Could not extract a mathematical "
                    "expression and answer."
                )
            }
        }


    # ====================================
    # FACT
    # ====================================

    else:

        print("========== FACT PATH ==========")

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

            print("Evidence:")
            print(evidence)

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
            "type": "FACT",
            "question": question,
            "answer": answer,
            "claims": verified_claims
        }