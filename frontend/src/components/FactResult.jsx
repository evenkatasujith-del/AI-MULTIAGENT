import React from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  XCircle,
  HelpCircle,
  Sparkles,
  ShieldCheck,
  FileText,
  Layers,
} from 'lucide-react';
import ClaimCard from './ClaimCard';
import StatusBadge from './StatusBadge';

export default function FactResult({ data }) {
  if (!data) return null;

  const question = data.question || '';
  const answer = data.answer || '';
  const claims = data.claims || [];

  // Compute summary metrics from backend data
  const totalClaims = claims.length;
  let stronglySupported = 0;
  let partiallyVerified = 0;
  let notVerified = 0;
  let risksDetected = 0;
  let totalConfidence = 0;

  claims.forEach((item) => {
    const dec = item.final_decision || item.verification || {};
    const st = String(dec.status || '').toUpperCase();
    const conf = Number(dec.confidence || 0);

    totalConfidence += conf;

    if (st === 'VERIFIED' || st === 'VERIFIED_AFTER_CORRECTION' || st === 'INDEPENDENTLY_SUPPORTED') {
      stronglySupported += 1;
    } else if (st === 'PARTIALLY_VERIFIED' || st === 'INDEPENDENTLY_PARTIAL') {
      partiallyVerified += 1;
    } else {
      notVerified += 1;
    }

    if (item.risk?.risk_detected) {
      risksDetected += 1;
    }
  });

  const avgConfidence = totalClaims > 0 ? Math.round((totalConfidence / totalClaims) * 100) : 0;

  // Determine overall status
  let overallStatus = 'NOT_VERIFIED';
  let overallLabel = 'Not Verified';

  if (totalClaims > 0) {
    if (stronglySupported === totalClaims) {
      overallStatus = 'VERIFIED';
      overallLabel = 'Verified';
    } else if (stronglySupported > 0 || partiallyVerified > 0) {
      overallStatus = 'PARTIALLY_VERIFIED';
      overallLabel = 'Partially Verified';
    } else {
      overallStatus = 'NOT_VERIFIED';
      overallLabel = 'Unverified';
    }
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
      </div>

      {/* Verification Summary Banner */}
      <div className="summary-banner">
        <div className="summary-score-circle">
          <span className="score-num">{avgConfidence}%</span>
          <span className="score-label">Confidence</span>
        </div>

        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-main)' }}>
              Verification Result
            </span>
            <StatusBadge status={overallStatus} label={overallLabel} />
            {risksDetected > 0 && (
              <span className="badge badge-unverified">
                {risksDetected} {risksDetected === 1 ? 'Risk Flagged' : 'Risks Flagged'}
              </span>
            )}
          </div>

          <p style={{ fontSize: '0.9rem', color: 'var(--text-subtle)', marginTop: '0.35rem' }}>
            {stronglySupported} of {totalClaims} claims independently confirmed via Wikipedia knowledge graph.
          </p>

          <div className="summary-metrics">
            <div className="metric-item">
              <span className="metric-val">{totalClaims}</span>
              <span className="metric-lbl">Claims Analyzed</span>
            </div>
            <div className="metric-item">
              <span className="metric-val" style={{ color: 'var(--status-verified-text)' }}>
                {stronglySupported}
              </span>
              <span className="metric-lbl">Strongly Supported</span>
            </div>
            <div className="metric-item">
              <span className="metric-val" style={{ color: 'var(--status-partial-text)' }}>
                {partiallyVerified}
              </span>
              <span className="metric-lbl">Partially Verified</span>
            </div>
            {notVerified > 0 && (
              <div className="metric-item">
                <span className="metric-val" style={{ color: 'var(--status-unverified-text)' }}>
                  {notVerified}
                </span>
                <span className="metric-lbl">Unverified / Rejected</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* AI Answer Card */}
      <div className="ai-answer-card">
        <div className="section-label">
          <Sparkles size={14} color="var(--primary-600)" />
          Generated AI Answer
        </div>
        <div className="ai-answer-body">
          {answer || 'No answer content received.'}
        </div>
      </div>

      {/* Claims Breakdown */}
      <div style={{ marginTop: '0.5rem' }}>
        <div className="claims-section-header">
          <div className="claims-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Layers size={18} color="var(--primary-600)" />
            <span>Claim-by-Claim Verification ({totalClaims})</span>
          </div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-subtle)' }}>
            Click any claim to inspect citations and independent verification
          </span>
        </div>

        {claims.length === 0 ? (
          <div className="detail-block" style={{ textAlign: 'center', padding: '2rem' }}>
            <p style={{ color: 'var(--text-subtle)' }}>No claims were extracted for verification.</p>
          </div>
        ) : (
          claims.map((claimItem, index) => (
            <ClaimCard key={index} claimData={claimItem} index={index} />
          ))
        )}
      </div>
    </div>
  );
}
