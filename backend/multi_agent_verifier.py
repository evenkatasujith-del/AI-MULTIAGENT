import os
import re
import json
import time
import concurrent.futures
import httpx
from dotenv import load_dotenv
from groq import Groq

# Ensure .env is freshly loaded
load_dotenv()

GROQ_MODEL = "openai/gpt-oss-20b"
GEMINI_MODEL = "gemini-1.5-flash"


def get_gemini_key(override_key: str = None) -> str:
    """Retrieve Gemini API key from parameter, env, or reloading .env."""
    if override_key and override_key.strip():
        return override_key.strip()

    load_dotenv(override=True)
    key = os.getenv("GEMINI_API_KEY", "")
    return key.strip() if key else ""


def get_groq_client():
    """Returns a cached or new Groq client using current GROQ_API_KEY."""
    load_dotenv(override=True)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


# ============================================================
# AGENT 1: GROQ VERIFICATION AGENT
# ============================================================

def verify_claim_with_groq(question: str, claim: str) -> dict:
    """
    Verifies a factual claim using Groq LLM agent.
    Returns verdict, confidence (0.0 to 1.0), explanation, and latency_ms.
    """
    client = get_groq_client()
    if not client:
        return {
            "agent": "Groq Agent",
            "model": GROQ_MODEL,
            "verdict": "ERROR",
            "confidence": 0.0,
            "explanation": "GROQ_API_KEY is missing from environment.",
            "latency_ms": 0.0,
            "status": "error"
        }

    prompt = f"""You are the Groq Verification Agent of VerifyAI.
Your task is to independently verify the following factual claim extracted from an AI-generated answer.

Context Question: {question}
Claim to Verify: "{claim}"

Evaluate whether this claim is factually true, partially true, or false based on established world knowledge.
Return ONLY a valid JSON object matching this schema:
{{
  "verdict": "VERIFIED" | "PARTIALLY_VERIFIED" | "CONTRADICTED" | "UNVERIFIED",
  "confidence": <float between 0.0 and 1.0>,
  "explanation": "<1-2 concise sentences explaining why the claim is true, partially true, or false>"
}}"""

    start_time = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a precise, objective verification agent. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        latency_ms = round((time.perf_counter() - start_time) * 1000, 1)

        raw = response.choices[0].message.content.strip()
        data = json.loads(raw)

        verdict = str(data.get("verdict", "VERIFIED")).upper()
        if verdict not in ["VERIFIED", "PARTIALLY_VERIFIED", "CONTRADICTED", "UNVERIFIED"]:
            verdict = "VERIFIED"

        try:
            confidence = float(data.get("confidence", 0.9))
            confidence = max(0.0, min(1.0, confidence))
        except (ValueError, TypeError):
            confidence = 0.85

        explanation = str(data.get("explanation", "Verified by Groq agent.")).strip()

        return {
            "agent": "Groq Agent",
            "model": GROQ_MODEL,
            "verdict": verdict,
            "confidence": round(confidence, 2),
            "explanation": explanation,
            "latency_ms": latency_ms,
            "status": "success"
        }

    except Exception as e:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 1)
        return {
            "agent": "Groq Agent",
            "model": GROQ_MODEL,
            "verdict": "UNVERIFIED",
            "confidence": 0.5,
            "explanation": f"Groq verification encountered an error: {str(e)}",
            "latency_ms": latency_ms,
            "status": "error"
        }


# ============================================================
# AGENT 2: GEMINI VERIFICATION AGENT
# ============================================================

def verify_claim_with_gemini(question: str, claim: str, override_key: str = None) -> dict:
    """
    Verifies a factual claim using Google Gemini LLM agent via REST API.
    Returns verdict, confidence (0.0 to 1.0), explanation, and latency_ms.
    """
    api_key = get_gemini_key(override_key)
    if not api_key:
        return {
            "agent": "Gemini Agent",
            "model": GEMINI_MODEL,
            "verdict": "CONFIG_REQUIRED",
            "confidence": None,
            "explanation": "GEMINI_API_KEY is not configured. Add your key in backend/.env to activate the Gemini agent.",
            "latency_ms": 0.0,
            "status": "key_missing"
        }

    prompt = f"""You are the Gemini Verification Agent of VerifyAI.
Your task is to independently verify the following factual claim extracted from an AI-generated answer.

Context Question: {question}
Claim to Verify: "{claim}"

Evaluate whether this claim is factually true, partially true, or false based on established world knowledge.
Return ONLY a valid JSON object matching this schema:
{{
  "verdict": "VERIFIED" | "PARTIALLY_VERIFIED" | "CONTRADICTED" | "UNVERIFIED",
  "confidence": <float between 0.0 and 1.0>,
  "explanation": "<1-2 concise sentences explaining why the claim is true, partially true, or false>"
}}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json"
        }
    }

    start_time = time.perf_counter()
    try:
        with httpx.Client(timeout=15.0) as http_client:
            res = http_client.post(url, json=payload)

        latency_ms = round((time.perf_counter() - start_time) * 1000, 1)

        if res.status_code != 200:
            err_msg = res.text
            try:
                err_json = res.json()
                if "error" in err_json and "message" in err_json["error"]:
                    err_msg = err_json["error"]["message"]
            except Exception:
                pass

            return {
                "agent": "Gemini Agent",
                "model": GEMINI_MODEL,
                "verdict": "ERROR",
                "confidence": 0.0,
                "explanation": f"Gemini API returned error: {err_msg}",
                "latency_ms": latency_ms,
                "status": "error"
            }

        res_data = res.json()
        raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        data = json.loads(raw_text)

        verdict = str(data.get("verdict", "VERIFIED")).upper()
        if verdict not in ["VERIFIED", "PARTIALLY_VERIFIED", "CONTRADICTED", "UNVERIFIED"]:
            verdict = "VERIFIED"

        try:
            confidence = float(data.get("confidence", 0.9))
            confidence = max(0.0, min(1.0, confidence))
        except (ValueError, TypeError):
            confidence = 0.85

        explanation = str(data.get("explanation", "Verified by Gemini agent.")).strip()

        return {
            "agent": "Gemini Agent",
            "model": GEMINI_MODEL,
            "verdict": verdict,
            "confidence": round(confidence, 2),
            "explanation": explanation,
            "latency_ms": latency_ms,
            "status": "success"
        }

    except Exception as e:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 1)
        return {
            "agent": "Gemini Agent",
            "model": GEMINI_MODEL,
            "verdict": "ERROR",
            "confidence": 0.0,
            "explanation": f"Gemini verification request failed: {str(e)}",
            "latency_ms": latency_ms,
            "status": "error"
        }


# ============================================================
# DUAL AGENT CLAIM VERIFICATION (CONCURRENT)
# ============================================================

def verify_claim_dual_agents(question: str, claim: str, gemini_key: str = None) -> dict:
    """
    Runs both Groq Agent and Gemini Agent concurrently on a single claim.
    Calculates Consensus, Confidence, and Latency for both agents.
    """
    wall_start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_groq = executor.submit(verify_claim_with_groq, question, claim)
        future_gemini = executor.submit(verify_claim_with_gemini, question, claim, gemini_key)

        groq_result = future_groq.result()
        gemini_result = future_gemini.result()

    total_latency_ms = round((time.perf_counter() - wall_start) * 1000, 1)

    # Compute consensus verdict and confidence
    active_confidences = []
    verdicts = []

    if groq_result.get("status") == "success":
        verdicts.append(groq_result["verdict"])
        active_confidences.append(groq_result["confidence"])

    if gemini_result.get("status") == "success":
        verdicts.append(gemini_result["verdict"])
        active_confidences.append(gemini_result["confidence"])

    if not active_confidences:
        consensus_confidence = 0.5
        consensus_verdict = "UNVERIFIED"
        agreement = "NO_AGENTS"
    elif len(active_confidences) == 1:
        consensus_confidence = active_confidences[0]
        consensus_verdict = verdicts[0]
        agreement = "SINGLE_AGENT"
    else:
        consensus_confidence = round(sum(active_confidences) / len(active_confidences), 2)
        if verdicts[0] == verdicts[1]:
            consensus_verdict = verdicts[0]
            agreement = "FULL_AGREEMENT"
        elif "CONTRADICTED" in verdicts:
            consensus_verdict = "DISCREPANCY_DETECTED"
            agreement = "DISAGREEMENT"
        elif "PARTIALLY_VERIFIED" in verdicts:
            consensus_verdict = "PARTIALLY_VERIFIED"
            agreement = "PARTIAL_AGREEMENT"
        else:
            consensus_verdict = "VERIFIED"
            agreement = "PARTIAL_AGREEMENT"

    return {
        "claim": claim,
        "consensus_verdict": consensus_verdict,
        "consensus_confidence": consensus_confidence,
        "agreement": agreement,
        "latency": {
            "groq_ms": groq_result.get("latency_ms", 0.0),
            "gemini_ms": gemini_result.get("latency_ms", 0.0),
            "total_ms": total_latency_ms
        },
        "agents": {
            "groq": groq_result,
            "gemini": gemini_result
        }
    }


# ============================================================
# DUAL AGENT MATH VERIFICATION
# ============================================================

def verify_math_with_groq(question: str, solution: str) -> dict:
    """Groq Agent evaluates mathematical steps, calculations, and final answer."""
    client = get_groq_client()
    if not client:
        return {"agent": "Groq Agent", "verdict": "ERROR", "confidence": 0.0, "latency_ms": 0.0, "status": "error"}

    prompt = f"""You are the Groq Math Verification Agent.
Check the mathematical correctness of this solution for the problem.

Problem: {question}
Proposed Solution:
{solution}

Analyze each step and the final answer.
Return ONLY JSON:
{{
  "verdict": "VERIFIED" | "INCORRECT",
  "confidence": <float 0.0 to 1.0>,
  "calculated_final": "<final number or value>",
  "explanation": "<brief assessment of steps and correctness>"
}}"""

    start_time = time.perf_counter()
    try:
        res = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        latency = round((time.perf_counter() - start_time) * 1000, 1)
        data = json.loads(res.choices[0].message.content)
        return {
            "agent": "Groq Agent",
            "model": GROQ_MODEL,
            "verdict": data.get("verdict", "VERIFIED"),
            "confidence": float(data.get("confidence", 0.95)),
            "calculated_final": data.get("calculated_final", ""),
            "explanation": data.get("explanation", ""),
            "latency_ms": latency,
            "status": "success"
        }
    except Exception as e:
        return {
            "agent": "Groq Agent",
            "model": GROQ_MODEL,
            "verdict": "ERROR",
            "confidence": 0.0,
            "explanation": str(e),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 1),
            "status": "error"
        }


def verify_math_with_gemini(question: str, solution: str, override_key: str = None) -> dict:
    """Gemini Agent evaluates mathematical steps, calculations, and final answer."""
    api_key = get_gemini_key(override_key)
    if not api_key:
        return {
            "agent": "Gemini Agent",
            "model": GEMINI_MODEL,
            "verdict": "CONFIG_REQUIRED",
            "confidence": None,
            "explanation": "GEMINI_API_KEY is not configured in backend/.env.",
            "latency_ms": 0.0,
            "status": "key_missing"
        }

    prompt = f"""You are the Gemini Math Verification Agent.
Check the mathematical correctness of this solution for the problem.

Problem: {question}
Proposed Solution:
{solution}

Analyze each step and the final answer.
Return ONLY JSON:
{{
  "verdict": "VERIFIED" | "INCORRECT",
  "confidence": <float 0.0 to 1.0>,
  "calculated_final": "<final number or value>",
  "explanation": "<brief assessment of steps and correctness>"
}}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
    }

    start_time = time.perf_counter()
    try:
        with httpx.Client(timeout=15.0) as http_client:
            res = http_client.post(url, json=payload)
        latency = round((time.perf_counter() - start_time) * 1000, 1)
        if res.status_code != 200:
            return {
                "agent": "Gemini Agent",
                "model": GEMINI_MODEL,
                "verdict": "ERROR",
                "confidence": 0.0,
                "explanation": f"HTTP {res.status_code}: {res.text}",
                "latency_ms": latency,
                "status": "error"
            }
        data = json.loads(res.json()["candidates"][0]["content"]["parts"][0]["text"])
        return {
            "agent": "Gemini Agent",
            "model": GEMINI_MODEL,
            "verdict": data.get("verdict", "VERIFIED"),
            "confidence": float(data.get("confidence", 0.95)),
            "calculated_final": data.get("calculated_final", ""),
            "explanation": data.get("explanation", ""),
            "latency_ms": latency,
            "status": "success"
        }
    except Exception as e:
        return {
            "agent": "Gemini Agent",
            "model": GEMINI_MODEL,
            "verdict": "ERROR",
            "confidence": 0.0,
            "explanation": str(e),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 1),
            "status": "error"
        }


def verify_math_dual_agents(question: str, solution: str, gemini_key: str = None) -> dict:
    """Runs Groq and Gemini concurrently on math problem and steps."""
    wall_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f_groq = executor.submit(verify_math_with_groq, question, solution)
        f_gemini = executor.submit(verify_math_with_gemini, question, solution, gemini_key)
        groq_res = f_groq.result()
        gemini_res = f_gemini.result()
    total_ms = round((time.perf_counter() - wall_start) * 1000, 1)

    confidences = [r["confidence"] for r in [groq_res, gemini_res] if r.get("confidence") is not None]
    avg_conf = round(sum(confidences) / len(confidences), 2) if confidences else 0.9

    return {
        "consensus_confidence": avg_conf,
        "latency": {
            "groq_ms": groq_res.get("latency_ms", 0.0),
            "gemini_ms": gemini_res.get("latency_ms", 0.0),
            "total_ms": total_ms
        },
        "agents": {
            "groq": groq_res,
            "gemini": gemini_res
        }
    }


# ============================================================
# DUAL AGENT CODE VERIFICATION
# ============================================================

def verify_code_with_groq(question: str, code: str) -> dict:
    """Groq Agent evaluates code logic, correctness, and edge cases."""
    client = get_groq_client()
    if not client:
        return {"agent": "Groq Agent", "verdict": "ERROR", "confidence": 0.0, "latency_ms": 0.0, "status": "error"}

    prompt = f"""You are the Groq Code Verification Agent.
Analyze this Python code written for the task:

Task: {question}
Code:
```python
{code}
```

Verify logic, syntax, and whether it satisfies the task.
Return ONLY JSON:
{{
  "verdict": "PASSED" | "FAILED",
  "confidence": <float 0.0 to 1.0>,
  "review": "<brief technical review of logic and safety>"
}}"""

    start_time = time.perf_counter()
    try:
        res = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        latency = round((time.perf_counter() - start_time) * 1000, 1)
        data = json.loads(res.choices[0].message.content)
        return {
            "agent": "Groq Agent",
            "model": GROQ_MODEL,
            "verdict": data.get("verdict", "PASSED"),
            "confidence": float(data.get("confidence", 0.95)),
            "review": data.get("review", "Code passed Groq static review."),
            "latency_ms": latency,
            "status": "success"
        }
    except Exception as e:
        return {
            "agent": "Groq Agent",
            "model": GROQ_MODEL,
            "verdict": "ERROR",
            "confidence": 0.0,
            "review": str(e),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 1),
            "status": "error"
        }


def verify_code_with_gemini(question: str, code: str, override_key: str = None) -> dict:
    """Gemini Agent evaluates code logic, correctness, and edge cases."""
    api_key = get_gemini_key(override_key)
    if not api_key:
        return {
            "agent": "Gemini Agent",
            "model": GEMINI_MODEL,
            "verdict": "CONFIG_REQUIRED",
            "confidence": None,
            "review": "GEMINI_API_KEY is not configured in backend/.env.",
            "latency_ms": 0.0,
            "status": "key_missing"
        }

    prompt = f"""You are the Gemini Code Verification Agent.
Analyze this Python code written for the task:

Task: {question}
Code:
```python
{code}
```

Verify logic, syntax, and whether it satisfies the task.
Return ONLY JSON:
{{
  "verdict": "PASSED" | "FAILED",
  "confidence": <float 0.0 to 1.0>,
  "review": "<brief technical review of logic and safety>"
}}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
    }

    start_time = time.perf_counter()
    try:
        with httpx.Client(timeout=15.0) as http_client:
            res = http_client.post(url, json=payload)
        latency = round((time.perf_counter() - start_time) * 1000, 1)
        if res.status_code != 200:
            return {
                "agent": "Gemini Agent",
                "model": GEMINI_MODEL,
                "verdict": "ERROR",
                "confidence": 0.0,
                "review": f"HTTP {res.status_code}: {res.text}",
                "latency_ms": latency,
                "status": "error"
            }
        data = json.loads(res.json()["candidates"][0]["content"]["parts"][0]["text"])
        return {
            "agent": "Gemini Agent",
            "model": GEMINI_MODEL,
            "verdict": data.get("verdict", "PASSED"),
            "confidence": float(data.get("confidence", 0.95)),
            "review": data.get("review", "Code passed Gemini static review."),
            "latency_ms": latency,
            "status": "success"
        }
    except Exception as e:
        return {
            "agent": "Gemini Agent",
            "model": GEMINI_MODEL,
            "verdict": "ERROR",
            "confidence": 0.0,
            "review": str(e),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 1),
            "status": "error"
        }


def verify_code_dual_agents(question: str, code: str, gemini_key: str = None) -> dict:
    """Runs Groq and Gemini concurrently on code task."""
    wall_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f_groq = executor.submit(verify_code_with_groq, question, code)
        f_gemini = executor.submit(verify_code_with_gemini, question, code, gemini_key)
        groq_res = f_groq.result()
        gemini_res = f_gemini.result()
    total_ms = round((time.perf_counter() - wall_start) * 1000, 1)

    confidences = [r["confidence"] for r in [groq_res, gemini_res] if r.get("confidence") is not None]
    avg_conf = round(sum(confidences) / len(confidences), 2) if confidences else 0.9

    return {
        "consensus_confidence": avg_conf,
        "latency": {
            "groq_ms": groq_res.get("latency_ms", 0.0),
            "gemini_ms": gemini_res.get("latency_ms", 0.0),
            "total_ms": total_ms
        },
        "agents": {
            "groq": groq_res,
            "gemini": gemini_res
        }
    }
