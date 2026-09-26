import React from 'react';
import {
  Calculator,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Cpu,
  ShieldCheck,
  Equal,
  Sparkles,
  Layers,
  Check,
} from 'lucide-react';
import StatusBadge from './StatusBadge';

export default function MathResult({ data }) {
  if (!data) return null;

  const question = data.question || '';
  const expression = data.expression || '';
  const fullAnswer = data.answer || '';
  const aiAnswer = data.ai_answer !== undefined ? data.ai_answer : fullAnswer;
  const verification = data.verification || {};

  const isVerified = Boolean(verification.verified);
  const calculated = verification.calculated !== undefined && verification.calculated !== null
    ? verification.calculated
    : (isVerified && verification.final_answer ? verification.final_answer : 'N/A');

  const reason = verification.reason || '';
  const status = verification.status || (isVerified ? 'VERIFIED' : 'INCORRECT');
  const steps = verification.steps || [];

  // Short display value for AI Answer box (avoid huge text squished in box)
  let aiAnswerDisplay = String(aiAnswer);
  if (aiAnswerDisplay.length > 35) {
    if (verification.final_answer) {
      aiAnswerDisplay = String(verification.final_answer);
    } else {
      aiAnswerDisplay = 'See Detailed Solution';
    }
  }

  // Calculated display
  let calculatedDisplay = String(calculated);
  if (calculatedDisplay.length > 35) {
    calculatedDisplay = String(verification.calculated ?? 'N/A');
  }

  return (
    <div className="result-container">
      {/* Question Header */}
      <div className="question-display-box">
        <div className="section-label">
          <HelpCircle size={14} color="var(--primary-600)" />
          Original Question
        </div>
        <p className="question-text">{question}</p>
        {expression && (
          <div style={{ marginTop: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-subtle)' }}>
              Primary Expression:
            </span>
            <code
              style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.85rem',
                background: 'var(--bg-card-subtle)',
                padding: '0.15rem 0.5rem',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-default)',
              }}
            >
              {expression}
            </code>
          </div>
        )}
      </div>

      {/* Verification Summary Card */}
      <div className="math-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Calculator size={20} color="var(--primary-600)" />
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-main)' }}>
              Mathematical Verification Engine
            </h3>
          </div>
          <StatusBadge status={status} />
        </div>

        {/* Side-by-side Comparison Grid */}
        <div className="math-comparison-grid">
          {/* AI Final Answer */}
          <div className="math-col">
            <span className="section-label">
              <Cpu size={13} />
              AI Answer
            </span>
            <div className="math-val-box">
              {aiAnswerDisplay}
            </div>
          </div>

          {/* Equal / Comparison Icon */}
          <div className="math-operator">
            <Equal size={20} />
          </div>

          {/* Independent AST Calculation */}
          <div className="math-col">
            <span className="section-label">
              <ShieldCheck size={13} color="var(--primary-600)" />
              Independent Calculation
            </span>
            <div
              className="math-val-box"
              style={{
                borderColor: isVerified ? 'var(--status-verified-border)' : 'var(--status-unverified-border)',
                background: isVerified ? 'var(--status-verified-bg)' : 'var(--status-unverified-bg)',
                color: isVerified ? 'var(--status-verified-text)' : 'var(--status-unverified-text)',
              }}
            >
              {calculatedDisplay}
            </div>
          </div>
        </div>

        {/* Verdict Banner */}
        <div className={`math-verdict-banner ${isVerified ? 'verified' : 'incorrect'}`}>
          {isVerified ? (
            <CheckCircle2 size={24} color="var(--status-verified-icon)" style={{ flexShrink: 0 }} />
          ) : (
            <XCircle size={24} color="var(--status-unverified-icon)" style={{ flexShrink: 0 }} />
          )}
          <div>
            <div style={{ fontWeight: 800, fontSize: '1rem', letterSpacing: '0.02em' }}>
              {isVerified ? '✓ INDEPENDENTLY VERIFIED' : '✕ CALCULATION MISMATCH'}
            </div>
            <p style={{ fontSize: '0.9rem', marginTop: '0.2rem', opacity: 0.9 }}>
              {reason ||
                (isVerified
                  ? 'All mathematical calculation steps were independently verified.'
                  : 'Independent calculation detected a discrepancy in the mathematical steps.')}
            </p>
          </div>
        </div>

        {/* Step-by-Step Verified Proof Steps */}
        {steps && steps.length > 0 && (
          <div style={{ marginTop: '1.25rem' }}>
            <div className="section-label" style={{ marginBottom: '0.5rem' }}>
              <Layers size={13} color="var(--primary-600)" />
              Independently Verified Steps ({steps.length})
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
              {steps.map((st, idx) => (
                <div
                  key={idx}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.55rem 0.85rem',
                    background: 'var(--bg-card-subtle)',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--border-light)',
                    fontSize: '0.85rem',
                    fontFamily: 'var(--font-mono)',
                  }}
                >
                  <span style={{ color: 'var(--text-main)' }}>
                    {st.expression} = {st.calculated}
                  </span>
                  <span
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.25rem',
                      color: st.verified ? 'var(--status-verified-text)' : 'var(--status-unverified-text)',
                      fontWeight: 600,
                      fontSize: '0.75rem',
                    }}
                  >
                    {st.verified ? <Check size={14} /> : <XCircle size={14} />}
                    {st.verified ? 'Verified' : 'Mismatch'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Dedicated AI Answer Card: Shows the full terminal answer on the website! */}
      {fullAnswer && (
        <div className="ai-answer-card">
          <div className="section-label">
            <Sparkles size={14} color="var(--primary-600)" />
            AI Step-by-Step Solution
          </div>
          <div className="ai-answer-body" style={{ whiteSpace: 'pre-wrap', lineHeight: 1.7 }}>
            {fullAnswer}
          </div>
        </div>
      )}
    </div>
  );
}
