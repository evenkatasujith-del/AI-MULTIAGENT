import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(name, question, expected_type):
    print(f"\n==========================================")
    print(f"RUNNING TEST: {name}")
    print(f"Question: {question}")
    print(f"Expected Type: {expected_type}")
    print(f"==========================================")

    response = requests.post(
        f"{BASE_URL}/smart-verify",
        json={"question": question},
        timeout=90
    )

    assert response.status_code == 200, f"HTTP Error {response.status_code}: {response.text}"
    data = response.json()

    print(f"Actual Detected Type: {data.get('type')}")
    assert data.get("type") == expected_type, f"Type mismatch! Expected {expected_type}, got {data.get('type')}"
    assert data.get("status") == "success", f"Status not success: {data}"

    if expected_type == "MATH":
        verification = data.get("verification", {})
        print(f"AI Answer: {data.get('ai_answer')}")
        print(f"Calculated: {verification.get('calculated')}")
        print(f"Math Status: {verification.get('status')}")
        print(f"Verified: {verification.get('verified')}")
        assert "verified" in verification, "Missing verified field in math verification"

    elif expected_type == "CODE":
        code = data.get("generated_code", "")
        execution = data.get("execution", {})
        print(f"Generated Code Lines: {len(code.splitlines())}")
        print(f"Execution Status: {execution.get('status')}")
        print(f"Execution Output: {execution.get('output')}")
        print(f"Execution Error: {execution.get('error')}")
        assert code, "No generated code returned"
        assert "status" in execution, "Missing status in execution"

    elif expected_type == "FACT":
        claims = data.get("claims", [])
        print(f"Answer Length: {len(data.get('answer', ''))}")
        print(f"Claims Extracted: {len(claims)}")
        if claims:
            first = claims[0]
            print(f"Claim 1: {first.get('claim')}")
            print(f"Claim 1 Decision: {first.get('final_decision')}")
            print(f"Claim 1 Sources Count: {len(first.get('evidence', {}).get('sources', []))}")
        assert data.get("answer"), "No answer returned"

    print(f"PASSED: {name}")
    return data

if __name__ == "__main__":
    print("Testing VerifyAI Unified Endpoint /smart-verify...")
    
    # 1. MATH Test
    test_endpoint("MATH: What is 25 * 16?", "What is 25 * 16?", "MATH")

    # 2. CODE Test
    test_endpoint("CODE: Give me Python code to find the largest number in a list", "Give me Python code to find the largest number in a list", "CODE")

    # 3. CODE Test with failure / intentional error
    test_endpoint("CODE: Write python code that raises a ZeroDivisionError", "Write python code that raises a ZeroDivisionError", "CODE")

    # 4. FACT Test
    test_endpoint("FACT: What is photosynthesis?", "What is photosynthesis?", "FACT")

    print("\nALL VERIFYAI ENDPOINT TESTS COMPLETED SUCCESSFULLY!")
