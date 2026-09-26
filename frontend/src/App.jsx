import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import QuestionInput from './components/QuestionInput';
import LoadingState from './components/LoadingState';
import FactResult from './components/FactResult';
import MathResult from './components/MathResult';
import CodeResult from './components/CodeResult';
import TechnicalDetails from './components/TechnicalDetails';
import HowItWorks from './components/HowItWorks';
import HistoryView from './components/HistoryView';
import ErrorBanner from './components/ErrorBanner';
import { verifyQuestion } from './api';
import { ArrowLeft, RotateCcw, Sparkles } from 'lucide-react';

const STORAGE_KEY = 'verifyai_history_v1';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [question, setQuestion] = useState('');
  const [pastedResponse, setPastedResponse] = useState('');
  const [geminiApiKey, setGeminiApiKey] = useState(() => {
    try {
      return localStorage.getItem('verifyai_gemini_api_key') || '';
    } catch {
      return '';
    }
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  // Sync geminiApiKey to localStorage
  useEffect(() => {
    try {
      if (geminiApiKey) {
        localStorage.setItem('verifyai_gemini_api_key', geminiApiKey);
      } else {
        localStorage.removeItem('verifyai_gemini_api_key');
      }
    } catch {
      // Ignore
    }
  }, [geminiApiKey]);

  // Load history from localStorage
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        setHistory(JSON.parse(stored));
      }
    } catch {
      // Ignore localStorage errors
    }
  }, []);

  // Save history item helper
  const saveToHistory = (itemResult, originalQuestion) => {
    try {
      const type = itemResult.type || 'FACT';
      let status = 'VERIFIED';
      let confidence = 0.9;

      if (type === 'FACT') {
        const claims = itemResult.claims || [];
        const hasUnverified = claims.some((c) => {
          const st = c.final_decision?.status || c.verification?.status;
          return st === 'NOT_VERIFIED' || st === 'REJECT';
        });
        status = hasUnverified ? 'PARTIALLY_VERIFIED' : 'VERIFIED';
        if (claims.length > 0) {
          const totalConf = claims.reduce((acc, c) => acc + (c.final_decision?.confidence || 0), 0);
          confidence = totalConf / claims.length;
        }
      } else if (type === 'MATH') {
        status = itemResult.verification?.status || (itemResult.verification?.verified ? 'VERIFIED' : 'INCORRECT');
        confidence = itemResult.verification?.verified ? 1.0 : 0.0;
      } else if (type === 'CODE') {
        status = itemResult.execution?.status || (itemResult.execution?.success ? 'PASSED' : 'FAILED');
        confidence = itemResult.execution?.success ? 1.0 : 0.0;
      }

      const newEntry = {
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        question: originalQuestion,
        type,
        status,
        confidence,
        rawResult: itemResult,
      };

      setHistory((prev) => {
        const updated = [newEntry, ...prev.filter((p) => p.question !== originalQuestion)].slice(0, 30);
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
        } catch {
          // LocalStorage full or private browsing
        }
        return updated;
      });
    } catch {
      // Handle silently
    }
  };

  const handleVerify = async () => {
    if (!question || !question.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const currentQ = question.trim();
      const currentR = pastedResponse.trim();
      const currentGeminiKey = geminiApiKey.trim();
      const data = await verifyQuestion(currentQ, currentR, currentGeminiKey);
      setResult(data);
      saveToHistory(data, currentQ);
    } catch (err) {
      setError(err.message || 'Verification failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuestion('');
    setPastedResponse('');
    setResult(null);
    setError(null);
  };

  const handleSelectHistoryItem = (item) => {
    setQuestion(item.question);
    setPastedResponse(item.rawResult?.pasted_response || '');
    setResult(item.rawResult);
    setError(null);
    setActiveTab('home');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleClearHistory = () => {
    if (window.confirm('Are you sure you want to clear your verification history?')) {
      setHistory([]);
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch {
        // Ignore
      }
    }
  };

  return (
    <div className="app-container">
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={(tab) => {
          setActiveTab(tab);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
        historyCount={history.length}
      />

      {/* Main Body */}
      <main className="main-content">
        {/* Error Banner */}
        {error && (
          <ErrorBanner
            error={error}
            onRetry={handleVerify}
            onDismiss={() => setError(null)}
          />
        )}

        {/* Tab 1: How It Works */}
        {activeTab === 'how-it-works' && (
          <HowItWorks onBackToDashboard={() => setActiveTab('home')} />
        )}

        {/* Tab 2: History */}
        {activeTab === 'history' && (
          <HistoryView
            historyItems={history}
            onSelectHistoryItem={handleSelectHistoryItem}
            onClearHistory={handleClearHistory}
            onBackToDashboard={() => setActiveTab('home')}
          />
        )}

        {/* Tab 3: Home / Verification Dashboard */}
        {activeTab === 'home' && (
          <>
            {/* If no result currently showing, show the hero input */}
            {!result && (
              <>
                <QuestionInput
                  question={question}
                  setQuestion={setQuestion}
                  pastedResponse={pastedResponse}
                  setPastedResponse={setPastedResponse}
                  geminiApiKey={geminiApiKey}
                  setGeminiApiKey={setGeminiApiKey}
                  onVerify={handleVerify}
                  loading={loading}
                  onClear={handleClear}
                />

                {loading && <LoadingState />}
              </>
            )}

            {/* If a result is available */}
            {result && (
              <div>
                {/* Result Top Action Bar */}
                <div className="result-header-card" style={{ marginBottom: '1.5rem' }}>
                  <button
                    type="button"
                    className="btn-secondary"
                    onClick={() => {
                      setResult(null);
                      window.scrollTo({ top: 0, behavior: 'smooth' });
                    }}
                  >
                    <ArrowLeft size={16} />
                    <span>Ask Another Question</span>
                  </button>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-subtle)' }}>
                      Detected Engine:
                    </span>
                    <span className={`result-type-tag ${String(result.type || 'fact').toLowerCase()}`}>
                      {result.type || 'FACT'}
                    </span>
                  </div>
                </div>

                {/* Loading indicator if user re-triggered */}
                {loading && <LoadingState />}

                {/* Specific UI based on response.type */}
                {result.type === 'FACT' && <FactResult data={result} />}
                {result.type === 'MATH' && <MathResult data={result} />}
                {result.type === 'CODE' && <CodeResult data={result} />}

                {/* Fallback if unknown type */}
                {result.type !== 'FACT' && result.type !== 'MATH' && result.type !== 'CODE' && (
                  <FactResult data={result} />
                )}

                {/* Collapsible Technical Details (Raw Backend JSON) */}
                <TechnicalDetails data={result} />

                {/* Bottom Back Button */}
                <div style={{ textAlign: 'center', marginTop: '2.5rem' }}>
                  <button
                    type="button"
                    className="btn-primary"
                    onClick={() => {
                      setResult(null);
                      setQuestion('');
                      window.scrollTo({ top: 0, behavior: 'smooth' });
                    }}
                  >
                    <Sparkles size={16} />
                    <span>Verify New Question</span>
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div style={{ maxWidth: '1040px', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div>
            <strong>VerifyAI</strong> — Multi-Agent AI Verification Platform
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-subtle)' }}>
            Wikipedia Grounding • Python AST Proofs • Subprocess Sandbox Execution
          </div>
        </div>
      </footer>
    </div>
  );
}
