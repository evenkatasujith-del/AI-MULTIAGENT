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

  const confidenceScore = decision.confidence ?? primary.confidence ?? 0;
  const decisionStatus = decision.status || primary.status || 'UNVERIFIED';

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
                Risk Detected
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
            {expanded ? 'Hide details' : 'View evidence'}
          </span>
          <ChevronDown
            size={18}
            className={`expand-chevron ${expanded ? 'open' : ''}`}
          />
        </div>
      </div>

      {expanded && (
        <div className="claim-details">
          {/* Decision Reason */}
          <div className="detail-block">
            <div className="detail-block-title">
              <span>Final Verification Decision</span>
              <StatusBadge status={decisionStatus} confidence={confidenceScore} showIcon={false} />
            </div>
            <div className="detail-block-content">
              <strong>Verdict: </strong>
              {decision.reason || primary.reason || 'No detailed reason provided.'}
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
                  Primary Verification
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
                  Independent Verifier
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

          {/* Risk & Correction */}
          {(risk.risk_detected || (correction && correction.corrected)) && (
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                gap: '1rem',
              }}
            >
              {/* Risk Info */}
              <div className="detail-block" style={{ borderColor: risk.risk_detected ? '#fecaca' : 'var(--border-default)' }}>
                <div className="detail-block-title">
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#b91c1c' }}>
                    <ShieldAlert size={14} />
                    Risk Analysis
                  </span>
                  <span>{risk.risk_detected ? 'Risks Detected' : 'Clear'}</span>
                </div>
                <div className="detail-block-content" style={{ fontSize: '0.85rem' }}>
                  {risk.risk_detected && risk.risks && risk.risks.length > 0 ? (
                    <ul style={{ paddingLeft: '1.2rem', color: '#991b1b' }}>
                      {risk.risks.map((r, i) => (
                        <li key={i}>{r}</li>
                      ))}
                    </ul>
                  ) : (
                    <span style={{ color: 'var(--text-subtle)' }}>No risks detected for this claim.</span>
                  )}
                </div>
              </div>

              {/* Correction Info */}
              {correction && correction.corrected && (
                <div className="detail-block" style={{ borderColor: '#fed7aa' }}>
                  <div className="detail-block-title">
                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#c2410c' }}>
                      <GitBranch size={14} />
                      Correction Engine ({correction.action})
                    </span>
                  </div>
                  <div className="detail-block-content" style={{ fontSize: '0.85rem' }}>
                    <p><strong>Action:</strong> {correction.action}</p>
                    <p style={{ marginTop: '0.25rem' }}><strong>Reason:</strong> {correction.reason}</p>
                    {correction.corrected_claim && (
                      <p style={{ marginTop: '0.25rem', color: 'var(--primary-800)' }}>
                        <strong>Corrected Claim:</strong> {correction.corrected_claim}
                      </p>
                    )}
                    {reverify && (
                      <p style={{ marginTop: '0.35rem', fontWeight: 600 }}>
                        Re-verification Status: {reverify.status} ({Math.round((reverify.confidence || 0) * 100)}%)
                      </p>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Evidence Sources Section */}
          <div className="detail-block">
            <div className="detail-block-title">
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <FileSearch size={14} color="var(--primary-600)" />
                Retrieved Wikipedia Evidence ({sources.length})
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
