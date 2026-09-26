import React, { useRef, useState } from 'react';
import {
  Sparkles,
  ArrowRight,
  Loader2,
  Check,
  RotateCcw,
  Zap,
  HelpCircle,
  FileCheck,
  ShieldCheck,
  Settings,
  Key,
} from 'lucide-react';

const EXAMPLES = [
  {
    type: 'fact',
    label: 'Fact Check',
    question: 'What is photosynthesis?',
  },
  {
    type: 'math',
    label: 'Math Calculation',
    question: 'What is 25 * 16?',
  },
  {
    type: 'code',
    label: 'Code Generation',
    question: 'Give me Python code to find the largest number in a list',
  },
  {
    type: 'fact',
    label: 'Science Fact',
    question: 'What is machine learning?',
  },
  {
    type: 'math',
    label: 'Validate AI Response',
    question: 'What is 144 / 12 + 7?',
    response: '144 / 12 is 12. Then 12 + 7 is 19. The final answer is 19.',
  },
];

export default function QuestionInput({
  question,
  setQuestion,
  pastedResponse = '',
  setPastedResponse = () => {},
  geminiApiKey = '',
  setGeminiApiKey = () => {},
  onVerify,
  loading,
  onClear,
}) {
  const [showApiConfig, setShowApiConfig] = useState(Boolean(geminiApiKey));
  const questionRef = useRef(null);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      if (!loading && question.trim()) {
        onVerify();
      }
    }
  };

  const handleSelectExample = (ex) => {
    setQuestion(ex.question);
    if (ex.response) {
      setPastedResponse(ex.response);
    } else {
      setPastedResponse('');
    }
    if (questionRef.current) {
      questionRef.current.focus();
    }
  };

  const hasPastedResponse = Boolean(pastedResponse && pastedResponse.trim());

  return (
    <div>
      {/* Hero Header */}
      <section className="hero-section">
        <div className="hero-tagline-badge">
          <Sparkles size={14} color="var(--primary-600)" />
          <span>Multi-Agent AI Verification Platform</span>
        </div>

        <h1 className="hero-title">
          AI Answers. <span className="highlight">Independently Verified.</span>
        </h1>

        <p className="hero-subtitle">
          Submit a question to generate a verified solution, or paste an external AI response to validate its accuracy against independent ground truth.
        </p>

        {/* Feature Checkmarks Strip */}
        <div className="features-strip">
          <div className="feature-pill">
            <span className="check">✓</span>
            <span>Fact Verification</span>
          </div>
          <div className="feature-pill">
            <span className="check">✓</span>
            <span>Mathematical Proofs</span>
          </div>
          <div className="feature-pill">
            <span className="check">✓</span>
            <span>Sandbox Code Execution</span>
          </div>
        </div>
      </section>

      {/* Main Dual-Input Card */}
      <div className="input-card">
        {/* Input 1: Question */}
        <div className="input-field-group">
          <div className="input-field-header">
            <label className="input-field-label">
              <HelpCircle size={15} color="var(--primary-600)" />
              <span>Question / Prompt</span>
              <span className="field-required">*</span>
            </label>
            <span className="field-hint-text">Required</span>
          </div>

          <div className="textarea-wrap">
            <textarea
              ref={questionRef}
              className="question-textarea"
              placeholder="Ask anything... (e.g. 'What is photosynthesis?' or 'What is 25 * 16?' or 'Write Python code to find the largest number in a list')"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
              rows={2}
            />
          </div>
        </div>

        {/* Divider */}
        <div className="input-field-divider" />

        {/* Input 2: External AI Response (Optional) */}
        <div className="input-field-group">
          <div className="input-field-header">
            <label className="input-field-label">
              <FileCheck size={15} color="var(--primary-600)" />
              <span>AI Response to Validate</span>
              <span className="field-optional-badge">Optional</span>
            </label>
            <span className="field-hint-text">
              {hasPastedResponse ? (
                <span style={{ color: 'var(--primary-700)', fontWeight: 600 }}>Validation Mode Active</span>
              ) : (
                'Leave blank to generate solution alone'
              )}
            </span>
          </div>

          <div className="response-box-wrap">
            <textarea
              className="question-textarea response-textarea"
              placeholder="Paste another AI's response here (e.g. from ChatGPT, Claude, DeepSeek) to validate its factual claims, math steps, or code... Leave empty if you just want VerifyAI to generate the solution alone."
              value={pastedResponse}
              onChange={(e) => setPastedResponse(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
              rows={3}
            />
          </div>
        </div>

        {/* Dual-Agent (Groq + Gemini) Configuration Drawer */}
        <div className="api-config-drawer">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
            <button
              type="button"
              className="api-config-toggle"
              onClick={() => setShowApiConfig(!showApiConfig)}
            >
              <Settings size={14} color="var(--primary-600)" />
              <span>
                Dual Agents: <strong>Groq (Active)</strong> + <strong>Gemini {geminiApiKey ? '(Key Added)' : '(.env)'}</strong>
              </span>
              <span style={{ fontSize: '0.7rem', color: 'var(--primary-700)', textDecoration: 'underline', marginLeft: '0.25rem' }}>
                {showApiConfig ? 'Hide Settings' : 'Configure Gemini Key'}
              </span>
            </button>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', color: 'var(--text-subtle)' }}>
              <span className="agent-status-badge active" style={{ fontSize: '0.68rem', padding: '0.1rem 0.4rem' }}>Groq Online</span>
              <span className={geminiApiKey ? "agent-status-badge active-gemini" : "agent-status-badge pending"} style={{ fontSize: '0.68rem', padding: '0.1rem 0.4rem' }}>
                {geminiApiKey ? 'Gemini Active' : 'Gemini via .env'}
              </span>
            </div>
          </div>

          {showApiConfig && (
            <div className="api-key-input-wrap">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                  <Key size={13} color="#3b82f6" />
                  Google Gemini API Key (Optional frontend override or backend/.env):
                </label>
                {geminiApiKey && (
                  <button
                    type="button"
                    onClick={() => setGeminiApiKey('')}
                    style={{ background: 'none', border: 'none', color: '#b91c1c', fontSize: '0.7rem', cursor: 'pointer', textDecoration: 'underline' }}
                  >
                    Clear Key
                  </button>
                )}
              </div>
              <input
                type="password"
                className="api-key-input"
                placeholder="Paste Gemini API Key here (e.g. AIzaSy...) or leave blank to use backend/.env"
                value={geminiApiKey}
                onChange={(e) => setGeminiApiKey(e.target.value)}
                disabled={loading}
              />
              <p style={{ fontSize: '0.72rem', color: 'var(--text-subtle)', marginTop: '0.35rem' }}>
                Both <strong>Groq</strong> and <strong>Gemini</strong> agents will verify your pasted response simultaneously and output individual Confidence, Claim assessment, and Latency metrics.
              </p>
            </div>
          )}
        </div>

        {/* Bottom Actions Bar */}
        <div className="input-actions">
          <div className="input-hint">
            {hasPastedResponse ? (
              <>
                <ShieldCheck size={15} color="var(--primary-600)" />
                <span style={{ color: 'var(--primary-700)', fontWeight: 600 }}>
                  Mode: Validating pasted response
                </span>
              </>
            ) : (
              <>
                <Zap size={14} color="var(--primary-600)" />
                <span>Mode: Auto-generate solution & verify</span>
              </>
            )}
          </div>

          <div className="btn-group">
            {(question || pastedResponse) && !loading && (
              <button
                type="button"
                className="btn-secondary"
                onClick={onClear}
                title="Clear inputs"
              >
                <RotateCcw size={14} />
                <span>Clear</span>
              </button>
            )}

            <button
              type="button"
              className="btn-primary"
              onClick={onVerify}
              disabled={loading || !question.trim()}
            >
              {loading ? (
                <>
                  <Loader2 size={18} className="loading-spinner" style={{ width: 18, height: 18, borderWidth: 2 }} />
                  <span>{hasPastedResponse ? 'Validating...' : 'Verifying...'}</span>
                </>
              ) : (
                <>
                  <span>{hasPastedResponse ? 'Validate Response' : 'Verify'}</span>
                  <ArrowRight size={17} />
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Example Questions Section */}
      <div className="examples-section">
        <div className="examples-title">
          <span>Try an example question:</span>
        </div>

        <div className="example-chips">
          {EXAMPLES.map((ex, idx) => (
            <button
              key={idx}
              type="button"
              className="example-chip"
              onClick={() => handleSelectExample(ex)}
              disabled={loading}
            >
              <span className={`example-tag ${ex.type}`}>{ex.type}</span>
              <span>"{ex.question}"</span>
              {ex.response && (
                <span
                  style={{
                    fontSize: '0.68rem',
                    background: 'var(--primary-100)',
                    color: 'var(--primary-700)',
                    padding: '0.1rem 0.35rem',
                    borderRadius: '4px',
                    fontWeight: 600,
                    marginLeft: '0.25rem',
                  }}
                >
                  + pasted response
                </span>
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
