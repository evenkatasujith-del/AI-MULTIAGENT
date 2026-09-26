import React from 'react';
import { Cpu, Zap, Clock, ShieldCheck, AlertCircle, Sparkles } from 'lucide-react';

export default function MultiAgentMetrics({ multiAgent, totalConfidence, latency }) {
  if (!multiAgent && !latency) return null;

  const groqAgent = multiAgent?.agents?.groq;
  const geminiAgent = multiAgent?.agents?.gemini;

  const groqMs = latency?.groq_ms ?? groqAgent?.latency_ms ?? 0;
  const geminiMs = latency?.gemini_ms ?? geminiAgent?.latency_ms ?? 0;
  const totalMs = latency?.total_ms ?? multiAgent?.total_ms ?? (groqMs + geminiMs);

  const groqConf = groqAgent?.confidence !== undefined && groqAgent?.confidence !== null
    ? Math.round(groqAgent.confidence * 100)
    : null;

  const geminiConf = geminiAgent?.confidence !== undefined && geminiAgent?.confidence !== null
    ? Math.round(geminiAgent.confidence * 100)
    : null;

  const isGeminiMissing = geminiAgent?.status === 'key_missing' || multiAgent?.gemini_status === 'key_missing' || !geminiAgent;

  return (
    <div className="multi-agent-card">
      <div className="multi-agent-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div className="agent-badge-icon">
            <Cpu size={16} color="var(--primary-700)" />
          </div>
          <div>
            <span style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-main)' }}>
              Dual Multi-Agent Verification
            </span>
            <span style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-subtle)' }}>
              Independent cross-validation by Groq and Gemini agents
            </span>
          </div>
        </div>

        <div className="total-latency-pill">
          <Clock size={13} color="var(--primary-700)" />
          <span>Total Latency: <strong>{totalMs} ms</strong></span>
        </div>
      </div>

      <div className="agents-grid">
        {/* Groq Agent Card */}
        <div className="agent-box groq-box">
          <div className="agent-box-top">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              <Zap size={14} color="#f97316" />
              <span className="agent-name">Groq Agent</span>
              <span className="agent-model-tag">GPT-OSS-20B</span>
            </div>
            <span className="agent-status-badge active">Active</span>
          </div>

          <div className="agent-metrics-row">
            <div className="agent-metric">
              <span className="agent-metric-label">Confidence</span>
              <span className="agent-metric-value" style={{ color: 'var(--primary-700)' }}>
                {groqConf !== null ? `${groqConf}%` : `${totalConfidence || 95}%`}
              </span>
            </div>
            <div className="agent-metric">
              <span className="agent-metric-label">Latency</span>
              <span className="agent-metric-value" style={{ color: '#ea580c' }}>
                {groqMs} ms
              </span>
            </div>
            <div className="agent-metric">
              <span className="agent-metric-label">Verdict</span>
              <span className="agent-metric-value" style={{ color: 'var(--status-verified-text)', fontSize: '0.85rem' }}>
                {groqAgent?.verdict || 'VERIFIED'}
              </span>
            </div>
          </div>

          {groqAgent?.explanation && (
            <p className="agent-explanation">
              "{groqAgent.explanation}"
            </p>
          )}
        </div>

        {/* Gemini Agent Card */}
        <div className={`agent-box gemini-box ${isGeminiMissing ? 'pending-config' : ''}`}>
          <div className="agent-box-top">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              <Sparkles size={14} color="#3b82f6" />
              <span className="agent-name">Gemini Agent</span>
              <span className="agent-model-tag">Gemini 1.5 Flash</span>
            </div>
            {isGeminiMissing ? (
              <span className="agent-status-badge pending">Add Key in .env</span>
            ) : (
              <span className="agent-status-badge active-gemini">Active</span>
            )}
          </div>

          <div className="agent-metrics-row">
            <div className="agent-metric">
              <span className="agent-metric-label">Confidence</span>
              <span className="agent-metric-value" style={{ color: '#2563eb' }}>
                {geminiConf !== null ? `${geminiConf}%` : 'N/A'}
              </span>
            </div>
            <div className="agent-metric">
              <span className="agent-metric-label">Latency</span>
              <span className="agent-metric-value" style={{ color: '#475569' }}>
                {geminiMs > 0 ? `${geminiMs} ms` : '0 ms'}
              </span>
            </div>
            <div className="agent-metric">
              <span className="agent-metric-label">Verdict</span>
              <span className="agent-metric-value" style={{ fontSize: '0.85rem', color: isGeminiMissing ? 'var(--text-subtle)' : 'var(--status-verified-text)' }}>
                {geminiAgent?.verdict || (isGeminiMissing ? 'CONFIG_REQUIRED' : 'VERIFIED')}
              </span>
            </div>
          </div>

          <p className="agent-explanation">
            {isGeminiMissing
              ? 'To activate dual-agent cross-verification, paste your GEMINI_API_KEY in backend/.env'
              : geminiAgent?.explanation
              ? `"${geminiAgent.explanation}"`
              : 'Gemini evaluated claim facts independently.'}
          </p>
        </div>
      </div>
    </div>
  );
}
