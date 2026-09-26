import React, { useState } from 'react';
import {
  ChevronDown,
  FileSearch,
  ShieldAlert,
  CheckCircle,
  Sparkles,
  GitBranch,
  Layers,
  ArrowRight,
  Clock,
  Zap,
  Cpu,
} from 'lucide-react';
import StatusBadge from './StatusBadge';
import EvidenceCard, { InsufficientEvidenceNotice } from './EvidenceCard';

export default function ClaimCard({ claimData, index }) {
  const [expanded, setExpanded] = useState(false);

  if (!claimData) return null;

  const claimText = claimData.claim;
  const decision = claimData.final_decision || {};
  const primary = claimData.verification || {};
  const independent = claimData.independent_verification || {};
  const risk = claimData.risk || {};
  const correction = claimData.correction || {};
  const reverify = claimData.re_verification;
  const evidence = claimData.evidence || {};
  const sources = evidence.sources || [];
  const dual = claimData.dual_agents;

  const confidenceScore = claimData.confidence ?? decision.confidence ?? primary.confidence ?? 0;
  const decisionStatus = dual?.consensus_verdict || decision.status || primary.status || 'UNVERIFIED';

  const groqAgent = dual?.agents?.groq;
  const geminiAgent = dual?.agents?.gemini;
  const latency = claimData.latency || dual?.latency || {};

  return (
    <div className="claim-card">
      <div className="claim-header" onClick={() => setExpanded(!expanded)}>
        <div className="claim-header-left">
          <div className="claim-tags-row">
            <span
              style={{
                fontSize: '0.75rem',
                fontWeight: 700,
                color: 'var(--text-subtle)',
                background: 'var(--bg-card-subtle)',
                padding: '0.15rem 0.5rem',
                borderRadius: 'var(--radius-sm)',
              }}
            >
              Claim #{index + 1}
            </span>

            <StatusBadge
              status={decisionStatus}
              confidence={confidenceScore}
            />

            {/* Confidence metric badge */}
            <span
              style={{
                fontSize: '0.75rem',
                fontWeight: 700,
                color: 'var(--primary-700)',
                background: 'var(--primary-50)',
                border: '1px solid var(--primary-200)',
                padding: '0.15rem 0.5rem',
                borderRadius: 'var(--radius-sm)',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.25rem',
              }}
            >
              <Cpu size={12} />
              {Math.round(confidenceScore * 100)}% Conf
            </span>

            {/* Latency metric pill */}
            {latency.total_ms !== undefined && (
              <span
                style={{
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  color: '#ea580c',
                  background: '#fff7ed',
                  border: '1px solid #ffedd5',
                  padding: '0.15rem 0.5rem',
                  borderRadius: 'var(--radius-sm)',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.25rem',
                }}
              >
                <Clock size={12} />
                {latency.total_ms} ms
              </span>
            )}

            {risk.risk_detected && (
              <span
                style={{
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  color: '#b91c1c',
                  background: '#fef2f2',
                  border: '1px solid #fecaca',
                  padding: '0.15rem 0.5rem',
                  borderRadius: '999px',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.25rem',
                }}
              >
                <ShieldAlert size={12} />
                Risk
              </span>
            )}

            <span
              style={{
                fontSize: '0.75rem',
                color: 'var(--text-subtle)',
                marginLeft: 'auto',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.25rem',
              }}
            >
              <FileSearch size={13} />
              {sources.length} {sources.length === 1 ? 'source' : 'sources'}
            </span>
          </div>

          <p className="claim-text">{claimText}</p>
        </div>

        <div className="claim-header-right">
          <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--primary-700)' }}>
            {expanded ? 'Hide details' : 'View breakdown'}
          </span>
          <ChevronDown
            size={18}
            className={`expand-chevron ${expanded ? 'open' : ''}`}
          />
        </div>
      </div>

      {expanded && (
        <div className="claim-details">
          {/* Dual Agents Verification Panel */}
          {dual && (
            <div className="detail-block" style={{ background: '#f8fafc', borderColor: '#e2e8f0' }}>
              <div className="detail-block-title">
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-main)' }}>
                  <Cpu size={15} color="var(--primary-600)" />
                  Dual Agents Verification (Groq vs Gemini)
                </span>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-subtle)' }}>
                  {dual.agreement === 'FULL_AGREEMENT' ? '✓ Full Agent Consensus' : 'Independent Assessment'}
                </span>
              </div>

              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                  gap: '0.75rem',
                  marginTop: '0.5rem',
                }}
              >
                {/* Groq Agent */}
                {groqAgent && (
                  <div
                    style={{
                      background: '#ffffff',
                      border: '1px solid var(--border-default)',
                      borderRadius: 'var(--radius-sm)',
                      padding: '0.75rem',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', fontWeight: 700, fontSize: '0.85rem' }}>
                        <Zap size={14} color="#f97316" />
                        Groq Agent
                      </span>
                      <div style={{ display: 'flex', gap: '0.35rem' }}>
                        <span style={{ fontSize: '0.72rem', background: '#fff7ed', color: '#c2410c', padding: '0.1rem 0.4rem', borderRadius: '4px', fontWeight: 600 }}>
                          {groqAgent.latency_ms} ms
                        </span>
                        <span style={{ fontSize: '0.72rem', background: 'var(--primary-50)', color: 'var(--primary-700)', padding: '0.1rem 0.4rem', borderRadius: '4px', fontWeight: 600 }}>
                          {Math.round((groqAgent.confidence || 0) * 100)}% Conf
                        </span>
                      </div>
                    </div>
                    <p style={{ fontSize: '0.825rem', color: 'var(--text-main)', lineHeight: 1.5 }}>
                      "{groqAgent.explanation}"
                    </p>
                  </div>
                )}

                {/* Gemini Agent */}
                {geminiAgent && (
                  <div
                    style={{
                      background: '#ffffff',
                      border: '1px solid var(--border-default)',
                      borderRadius: 'var(--radius-sm)',
                      padding: '0.75rem',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', fontWeight: 700, fontSize: '0.85rem' }}>
                        <Sparkles size={14} color="#3b82f6" />
                        Gemini Agent
                      </span>
                      <div style={{ display: 'flex', gap: '0.35rem' }}>
                        <span style={{ fontSize: '0.72rem', background: '#eff6ff', color: '#1d4ed8', padding: '0.1rem 0.4rem', borderRadius: '4px', fontWeight: 600 }}>
                          {geminiAgent.latency_ms > 0 ? `${geminiAgent.latency_ms} ms` : '0 ms'}
                        </span>
                        {geminiAgent.confidence !== null && (
                          <span style={{ fontSize: '0.72rem', background: 'var(--primary-50)', color: 'var(--primary-700)', padding: '0.1rem 0.4rem', borderRadius: '4px', fontWeight: 600 }}>
                            {Math.round((geminiAgent.confidence || 0) * 100)}% Conf
                          </span>
                        )}
                      </div>
                    </div>
                    <p style={{ fontSize: '0.825rem', color: geminiAgent.status === 'key_missing' ? 'var(--text-subtle)' : 'var(--text-main)', lineHeight: 1.5 }}>
                      {geminiAgent.explanation}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Decision Reason */}
          <div className="detail-block">
            <div className="detail-block-title">
              <span>Final Verification Decision</span>
              <StatusBadge status={decisionStatus} confidence={confidenceScore} showIcon={false} />
            </div>
            <div className="detail-block-content">
              <strong>Verdict: </strong>
              {decision.reason || primary.reason || 'Verified based on consensus and factual citations.'}
            </div>
          </div>

          {/* Verification Signals (Primary vs Independent) */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '1rem',
            }}
          >
            {/* Primary Verification */}
            <div className="detail-block">
              <div className="detail-block-title">
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <Layers size={14} color="var(--primary-600)" />
                  Knowledge Graph Verification
                </span>
                <StatusBadge status={primary.status} confidence={primary.confidence} showIcon={false} />
              </div>
              <div className="detail-block-content" style={{ fontSize: '0.85rem' }}>
                <p><strong>Reason:</strong> {primary.reason || 'N/A'}</p>
                {primary.supporting_source && (
                  <p style={{ marginTop: '0.35rem' }}>
                    <strong>Top Source:</strong> {primary.supporting_source}
                  </p>
                )}
              </div>
            </div>

            {/* Independent Verification */}
            <div className="detail-block">
              <div className="detail-block-title">
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <CheckCircle size={14} color="#0284c7" />
                  Independent Proof Verifier
                </span>
                <StatusBadge status={independent.status} confidence={independent.confidence} showIcon={false} />
              </div>
              <div className="detail-block-content" style={{ fontSize: '0.85rem' }}>
                <p><strong>Assessment:</strong> {independent.reason || 'No independent record.'}</p>
                {independent.evidence_sentence && (
                  <p
                    style={{
                      marginTop: '0.4rem',
                      fontStyle: 'italic',
                      color: 'var(--text-muted)',
                      borderLeft: '2px solid var(--primary-300)',
                      paddingLeft: '0.5rem',
                    }}
                  >
                    "{independent.evidence_sentence}"
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Evidence Sources Section */}
          <div className="detail-block">
            <div className="detail-block-title">
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <FileSearch size={14} color="var(--primary-600)" />
                Retrieved Ground-Truth Evidence ({sources.length})
              </span>
              <span style={{ fontSize: '0.75rem', fontWeight: 500, color: 'var(--text-subtle)' }}>
                Status: {evidence.status || 'N/A'}
              </span>
            </div>

            {sources.length === 0 ? (
              <InsufficientEvidenceNotice message={evidence.message} />
            ) : (
              <div className="evidence-grid">
                {sources.map((source, sIdx) => (
                  <EvidenceCard key={sIdx} source={source} />
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
