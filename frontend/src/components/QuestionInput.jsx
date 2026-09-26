import React, { useRef } from 'react';
import {
  Sparkles,
  ArrowRight,
  Loader2,
  Check,
  RotateCcw,
  Zap,
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
    label: 'Code Generation & Execution',
    question: 'Give me Python code to find the largest number in a list',
  },
  {
    type: 'fact',
    label: 'Science Fact',
    question: 'What is machine learning?',
  },
  {
    type: 'math',
    label: 'Algebra',
    question: 'What is 144 / 12 + 7?',
  },
];

export default function QuestionInput({
  question,
  setQuestion,
  onVerify,
  loading,
  onClear,
}) {
  const textareaRef = useRef(null);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey || !e.shiftKey)) {
      e.preventDefault();
      if (!loading && question.trim()) {
        onVerify();
      }
    }
  };

  const handleSelectExample = (exQuestion) => {
    setQuestion(exQuestion);
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };

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
          Submit any fact, math expression, or coding task. VerifyAI automatically detects the question type and runs independent multi-agent verification.
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

      {/* Main Input Box Card */}
      <div className="input-card">
        <div className="textarea-wrap">
          <textarea
            ref={textareaRef}
            className="question-textarea"
            placeholder="Ask anything... (e.g. 'What is photosynthesis?' or 'What is 25 * 16?' or 'Write Python code to find the largest number')"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            rows={3}
          />
        </div>

        <div className="input-actions">
          <div className="input-hint">
            <Zap size={14} color="var(--primary-600)" />
            <span>Automatic type classification (FACT • MATH • CODE)</span>
          </div>

          <div className="btn-group">
            {question && !loading && (
              <button
                type="button"
                className="btn-secondary"
                onClick={onClear}
                title="Clear question"
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
                  <span>Verifying...</span>
                </>
              ) : (
                <>
                  <span>Verify</span>
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
              onClick={() => handleSelectExample(ex.question)}
              disabled={loading}
            >
              <span className={`example-tag ${ex.type}`}>{ex.type}</span>
              <span>"{ex.question}"</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
