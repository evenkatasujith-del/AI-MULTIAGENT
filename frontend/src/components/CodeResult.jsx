import React, { useState } from 'react';
import {
  Code,
  Terminal,
  CheckCircle2,
  XCircle,
  Copy,
  Check,
  HelpCircle,
  AlertTriangle,
  Play,
  RotateCcw,
} from 'lucide-react';
import StatusBadge from './StatusBadge';

/**
 * Basic Python syntax highlighter that parses lines into colored tokens
 * (keywords, def, strings, comments, numbers) safely without extra heavy dependencies.
 */
function renderPythonLine(line) {
  // Regex tokens
  const pythonKeywords = new Set([
    'def', 'return', 'if', 'else', 'elif', 'for', 'while', 'in', 'not', 'and', 'or',
    'is', 'class', 'import', 'from', 'as', 'try', 'except', 'finally', 'raise',
    'with', 'lambda', 'pass', 'break', 'continue', 'yield', 'True', 'False', 'None'
  ]);

  // Check for whole-line comment
  const trimmed = line.trim();
  if (trimmed.startsWith('#')) {
    return <span style={{ color: '#64748b', fontStyle: 'italic' }}>{line}</span>;
  }

  // Tokenize line preserving spaces
  const tokens = line.split(/(\b[a-zA-Z_]\w*\b|"[^"]*"|'[^']*'|#.*|\d+|[^\w\s])/g);

  return tokens.map((token, i) => {
    if (!token) return null;

    if (token.startsWith('#')) {
      return <span key={i} style={{ color: '#64748b', fontStyle: 'italic' }}>{token}</span>;
    }
    if ((token.startsWith('"') && token.endsWith('"')) || (token.startsWith("'") && token.endsWith("'"))) {
      return <span key={i} style={{ color: '#34d399' }}>{token}</span>;
    }
    if (pythonKeywords.has(token)) {
      return <span key={i} style={{ color: '#60a5fa', fontWeight: 600 }}>{token}</span>;
    }
    if (/^\d+(\.\d+)?$/.test(token)) {
      return <span key={i} style={{ color: '#f59e0b' }}>{token}</span>;
    }
    if (token === 'print' || token === 'len' || token === 'range' || token === 'int' || token === 'str' || token === 'list') {
      return <span key={i} style={{ color: '#c084fc' }}>{token}</span>;
    }
    return <span key={i}>{token}</span>;
  });
}

export default function CodeResult({ data }) {
  const [copied, setCopied] = useState(false);

  if (!data) return null;

  const question = data.question || '';
  let rawCode = data.generated_code || '';

  // Clean unescaped newlines if code was doubly-escaped
  if (typeof rawCode === 'string') {
    // If literal '\n' characters exist instead of actual newlines
    if (rawCode.includes('\\n') && !rawCode.includes('\n')) {
      rawCode = rawCode.replace(/\\n/g, '\n').replace(/\\t/g, '    ');
    }
  }

  const execution = data.execution || {};
  const isPassed = Boolean(execution.success || execution.status === 'PASSED');
  const executionStatus = execution.status || (isPassed ? 'PASSED' : 'FAILED');
  const stdout = execution.output || '';
  const stderr = execution.error || '';
  const correction = data.correction;

  const lines = rawCode.split('\n');

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(rawCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
    }
  };

  return (
    <div className="result-container">
      {/* Question Header */}
      <div className="question-display-box">
        <div className="section-label">
          <HelpCircle size={14} color="var(--primary-600)" />
          Original Request
        </div>
        <p className="question-text">{question}</p>
      </div>

      {/* Code Editor Block */}
      <div className="code-editor-card">
        <div className="code-header-bar">
          <div className="code-lang-tag">
            <Code size={16} color="#38bdf8" />
            <span>Python 3 Sandbox</span>
          </div>

          <button type="button" className="btn-copy" onClick={handleCopy}>
            {copied ? (
              <>
                <Check size={13} color="#4ade80" />
                <span style={{ color: '#4ade80' }}>Copied!</span>
              </>
            ) : (
              <>
                <Copy size={13} />
                <span>Copy Code</span>
              </>
            )}
          </button>
        </div>

        <div className="code-block-wrap">
          <pre className="code-pre">
            {lines.map((line, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'baseline',
                  lineHeight: '1.6',
                }}
              >
                <span
                  style={{
                    display: 'inline-block',
                    width: '38px',
                    userSelect: 'none',
                    textAlign: 'right',
                    marginRight: '16px',
                    color: '#475569',
                    fontSize: '0.8rem',
                  }}
                >
                  {idx + 1}
                </span>
                <span style={{ flex: 1, whiteSpace: 'pre' }}>
                  {renderPythonLine(line)}
                </span>
              </div>
            ))}
          </pre>
        </div>
      </div>

      {/* Sandbox Execution Result */}
      <div className="terminal-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Terminal size={18} color="var(--primary-600)" />
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-main)' }}>
              Sandbox Execution Result
            </h3>
          </div>
          <StatusBadge status={executionStatus} />
        </div>

        {/* Stdout Output */}
        {stdout && (
          <div style={{ marginTop: '1rem' }}>
            <span className="section-label">
              <Play size={12} color="var(--primary-600)" />
              Output (STDOUT)
            </span>
            <div className="terminal-box">
              {stdout}
            </div>
          </div>
        )}

        {/* Stderr or Error Output */}
        {stderr && (
          <div style={{ marginTop: '1rem' }}>
            <span className="section-label" style={{ color: '#b91c1c' }}>
              <AlertTriangle size={12} color="#dc2626" />
              Execution Error (STDERR)
            </span>
            <div className="terminal-box error">
              {stderr}
            </div>
          </div>
        )}

        {/* If no stdout or stderr */}
        {!stdout && !stderr && (
          <div className="terminal-box" style={{ color: '#94a3b8' }}>
            Code executed with return code 0 (no output printed to stdout).
          </div>
        )}

        {/* Correction Feedback */}
        {correction && (
          <div
            style={{
              marginTop: '1rem',
              padding: '0.85rem 1rem',
              background: '#fef2f2',
              border: '1px solid #fecaca',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.85rem',
              color: '#991b1b',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            <RotateCcw size={16} />
            <span>{correction.message || 'Execution error detected during automated test.'}</span>
          </div>
        )}
      </div>
    </div>
  );
}
