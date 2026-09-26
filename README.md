# VerifyAI — Multi-Agent AI Verification Platform

> **AI Answers. Independently Verified.**

VerifyAI is a multi-agent verification system designed to eradicate AI hallucinations by cross-examining generated answers through domain-specific, independent verification pipelines.

---

## Architecture Overview

The repository is organized into dedicated **`frontend/`** and **`backend/`** directories:

```
AI-MULTIAGENT/
├── backend/
│   ├── main.py                     # FastAPI server with /smart-verify endpoint
│   ├── ai.py                       # Generator & Claim Extraction agents (Groq)
│   ├── router.py                   # Automatic question classification (FACT / MATH / CODE)
│   ├── evidence.py                 # Wikipedia API knowledge graph evidence retrieval
│   ├── verifier.py                 # Primary claim verification engine
│   ├── independent_verifier.py     # Independent verification engine
│   ├── risk_detector.py            # Contradiction and hallucination risk detection
│   ├── correction.py               # Claim correction and qualification
│   ├── reverify.py                 # Re-verification for qualified claims
│   ├── decision.py                 # Multi-signal final decision synthesis
│   ├── math_verifier.py            # AST deterministic math calculation engine
│   ├── code_sandbox.py             # Isolated Python subprocess execution sandbox
│   ├── requirements.txt            # Python dependencies
│   └── test_e2e_api.py             # E2E test suite
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx          # Top navigation with live backend status indicator
│   │   │   ├── QuestionInput.jsx   # Hero search box, example chips, verification triggers
│   │   │   ├── LoadingState.jsx    # Multi-step progress animation
│   │   │   ├── FactResult.jsx      # Summary metrics, AI answer card, claim-by-claim cards
│   │   │   ├── ClaimCard.jsx       # Expandable card with dual verifiers, risks, evidence
│   │   │   ├── EvidenceCard.jsx    # Wikipedia source cards with relevance & direct links
│   │   │   ├── MathResult.jsx      # Side-by-side AI answer vs independent calculation
│   │   │   ├── CodeResult.jsx      # Syntax-highlighted code editor + execution terminal
│   │   │   ├── StatusBadge.jsx     # Standardized status badge component
│   │   │   ├── TechnicalDetails.jsx# Formatted raw JSON viewer for evaluators
│   │   │   ├── HowItWorks.jsx      # Architecture flowchart & engine explanations
│   │   │   ├── HistoryView.jsx     # LocalStorage history browser
│   │   │   └── ErrorBanner.jsx     # User-friendly error & retry notices
│   │   ├── api.js                  # Centralized API client connected to backend
│   │   ├── App.jsx                 # Core application controller
│   │   └── index.css               # Modern light green + white design system
│   ├── index.html                  # HTML entry point with Inter & JetBrains Mono fonts
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## Verification Engines

1. **FACT Engine**
   - **Generation**: AI answer synthesis with claim extraction (up to 6 atomic factual claims).
   - **Evidence Retrieval**: Live Wikipedia search and summary retrieval for relevant topics.
   - **Dual Verification**: Primary verifier + Independent verifier evaluate evidence alignment.
   - **Risk Detection**: Contradiction identification, overgeneralization check, and unsupported claim flagging.
   - **Correction & Re-verification**: Automatic qualification and re-evaluation before the final verdict.

2. **MATH Engine**
   - **Expression Extraction**: Automatically extracts the mathematical expression from the question.
   - **Deterministic Proof**: Evaluates the expression using Python's Abstract Syntax Tree (`ast`) module in a restricted sandbox.
   - **Comparison**: Verifies whether the AI answer matches the mathematical ground truth within float tolerance.

3. **CODE Engine**
   - **Synthesis**: Generates clean, executable Python solutions.
   - **Sandbox Execution**: Executes the code in a dedicated temporary subprocess sandbox with timeout isolation.
   - **Verification**: Audits standard output (STDOUT), standard error (STDERR), and exit codes.

---

## Quickstart

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```
- API Base URL: `http://127.0.0.1:8000`
- Swagger Docs: `http://127.0.0.1:8000/docs`

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
- Frontend UI: `http://127.0.0.1:5173`
- Pre-configured backend connection: `VITE_API_URL=http://127.0.0.1:8000`

---

## Running the E2E Test Suite
```bash
python backend/test_e2e_api.py
```
This tests:
- `What is 25 * 16?` (MATH: verified match)
- `Give me Python code to find the largest number in a list` (CODE: sandbox execution passed)
- `Write python code that raises a ZeroDivisionError` (CODE: sandbox execution error handling)
- `What is photosynthesis?` (FACT: live Wikipedia claim verification)
