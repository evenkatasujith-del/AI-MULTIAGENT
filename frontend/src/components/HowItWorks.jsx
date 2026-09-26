import React from 'react';
import {
  HelpCircle,
  Cpu,
  ShieldCheck,
  Search,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Sparkles,
  ArrowDown,
  Calculator,
  Code2,
  BookOpen,
} from 'lucide-react';

const PIPELINE_STEPS = [
  {
    step: '1',
    title: 'Question Classification',
    desc: 'The incoming prompt is automatically analyzed by the router agent to classify it into FACT, MATH, or CODE. Users never need to manually configure modes.',
    icon: HelpCircle,
  },
  {
    step: '2',
    title: 'AI Generation',
    desc: 'A domain-specific generator agent synthesizes a high-fidelity factual answer, numerical result, or clean Python script using optimized low-temperature inference.',
    icon: Cpu,
  },
  {
    step: '3',
    title: 'Independent Verification',
    desc: 'An independent verifier checks the AI output without bias. For facts, claims are matched against live Wikipedia sources. For math, an AST parser computes the answer. For code, a secure sandbox runs the script.',
    icon: Search,
  },
  {
    step: '4',
    title: 'Risk & Contradiction Detection',
    desc: 'The risk detector analyzes primary and independent verification signals to uncover logical contradictions, unsupported statements, or missing evidence.',
    icon: AlertTriangle,
  },
  {
    step: '5',
    title: 'Correction & Re-verification',
    desc: 'If risk is detected, the correction engine attempts to qualify or reject the statement. Qualified statements undergo re-verification before reaching the final decision.',
    icon: RotateCcw,
  },
  {
    step: '6',
    title: 'Multi-Signal Final Decision',
    desc: 'All verification signals, confidence scores, and evidence sources are combined into a transparent verdict (VERIFIED, PARTIALLY VERIFIED, or NOT VERIFIED).',
    icon: ShieldCheck,
  },
];

export default function HowItWorks({ onBackToDashboard }) {
  return (
    <div className="how-it-works-wrap">
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
        <div className="hero-tagline-badge">
          <BookOpen size={14} color="var(--primary-600)" />
          <span>System Architecture</span>
        </div>
        <h2 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-main)' }}>
          How VerifyAI Works
        </h2>
        <p style={{ color: 'var(--text-subtle)', maxWidth: '640px', margin: '0.5rem auto 0' }}>
          VerifyAI prevents AI hallucinations by decoupling generation from independent verification across three specialized domain engines.
        </p>
      </div>

      {/* The 3 Specialized Pathways */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1.25rem',
        }}
      >
        {/* FACT Engine */}
        <div className="flow-step-card" style={{ borderTop: '4px solid #0284c7' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
            <div
              style={{
                width: 32,
                height: 32,
                borderRadius: '8px',
                background: '#e0f2fe',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#0369a1',
              }}
            >
              <BookOpen size={18} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)' }}>
                1. Fact Engine
              </h3>
              <span style={{ fontSize: '0.75rem', color: '#0369a1', fontWeight: 600 }}>
                KNOWLEDGE GRAPH VERIFICATION
              </span>
            </div>
          </div>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
            Extracts individual claims from the AI answer, fetches live Wikipedia knowledge articles, and cross-checks every sentence with dual primary + independent verifiers.
          </p>
          <div
            style={{
              marginTop: '1rem',
              padding: '0.75rem',
              background: '#f0f9ff',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.8rem',
              color: '#0369a1',
              fontWeight: 500,
            }}
          >
            AI → Claim Extraction → Wikipedia Evidence → Dual Verification → Risk Detection → Final Decision
          </div>
        </div>

        {/* MATH Engine */}
        <div className="flow-step-card" style={{ borderTop: '4px solid #d97706' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
            <div
              style={{
                width: 32,
                height: 32,
                borderRadius: '8px',
                background: '#fef3c7',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#b45309',
              }}
            >
              <Calculator size={18} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)' }}>
                2. Math Engine
              </h3>
              <span style={{ fontSize: '0.75rem', color: '#b45309', fontWeight: 600 }}>
                AST DETERMINISTIC PROOFS
              </span>
            </div>
          </div>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
            Extracts mathematical expressions and evaluates them using a safe Abstract Syntax Tree (AST) arithmetic engine, comparing the AI answer with mathematical ground truth.
          </p>
          <div
            style={{
              marginTop: '1rem',
              padding: '0.75rem',
              background: '#fffbeb',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.8rem',
              color: '#b45309',
              fontWeight: 500,
            }}
          >
            AI → Expression Extraction → Safe AST Math Engine → Tolerance Comparison → Verification
          </div>
        </div>

        {/* CODE Engine */}
        <div className="flow-step-card" style={{ borderTop: '4px solid var(--primary-600)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
            <div
              style={{
                width: 32,
                height: 32,
                borderRadius: '8px',
                background: 'var(--primary-50)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--primary-700)',
              }}
            >
              <Code2 size={18} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)' }}>
                3. Code Engine
              </h3>
              <span style={{ fontSize: '0.75rem', color: 'var(--primary-700)', fontWeight: 600 }}>
                ISOLATED SANDBOX EXECUTION
              </span>
            </div>
          </div>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
            Generates clean Python code and immediately runs it inside an isolated subprocess sandbox. Evaluates return codes, standard output, exceptions, and timeouts.
          </p>
          <div
            style={{
              marginTop: '1rem',
              padding: '0.75rem',
              background: 'var(--primary-50)',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.8rem',
              color: 'var(--primary-800)',
              fontWeight: 500,
            }}
          >
            AI → Python Code Generation → Subprocess Sandbox Run → STDOUT / Error Audit → Result
          </div>
        </div>
      </div>

      {/* Sequential Pipeline Flowchart */}
      <div style={{ marginTop: '1.5rem' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '1.25rem', textAlign: 'center' }}>
          End-to-End Multi-Agent Pipeline
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', maxWidth: '680px', margin: '0 auto' }}>
          {PIPELINE_STEPS.map((s, idx) => {
            const Icon = s.icon;
            return (
              <React.Fragment key={s.step}>
                <div
                  className="flow-step-card"
                  style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '1rem',
                    padding: '1.15rem 1.25rem',
                  }}
                >
                  <div
                    style={{
                      width: 36,
                      height: 36,
                      borderRadius: '50%',
                      background: 'var(--primary-50)',
                      border: '2px solid var(--primary-500)',
                      color: 'var(--primary-700)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 800,
                      fontSize: '0.95rem',
                      flexShrink: 0,
                    }}
                  >
                    {s.step}
                  </div>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <Icon size={16} color="var(--primary-600)" />
                      <h4 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-main)' }}>
                        {s.title}
                      </h4>
                    </div>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.25rem', lineHeight: 1.5 }}>
                      {s.desc}
                    </p>
                  </div>
                </div>

                {idx < PIPELINE_STEPS.length - 1 && (
                  <div className="flow-arrow">
                    <ArrowDown size={20} />
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>

      {/* Back to dashboard button */}
      <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
        <button
          type="button"
          className="btn-primary"
          onClick={onBackToDashboard}
        >
          <Sparkles size={16} />
          <span>Try a Verification Now</span>
        </button>
      </div>
    </div>
  );
}
