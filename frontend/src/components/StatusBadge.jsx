import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, AlertCircle, Clock } from 'lucide-react';

export default function StatusBadge({ status, label, confidence = null, showIcon = true }) {
  if (!status) return null;

  const normalized = String(status).toUpperCase();

  let badgeClass = 'badge-neutral';
  let IconComponent = AlertCircle;
  let displayLabel = label || status.replace(/_/g, ' ');

  if (
    normalized === 'VERIFIED' ||
    normalized === 'VERIFIED_AFTER_CORRECTION' ||
    normalized === 'PASSED' ||
    normalized === 'INDEPENDENTLY_SUPPORTED' ||
    normalized === 'ACCEPT'
  ) {
    badgeClass = 'badge-verified';
    IconComponent = CheckCircle2;
  } else if (
    normalized === 'PARTIALLY_VERIFIED' ||
    normalized === 'INDEPENDENTLY_PARTIAL' ||
    normalized === 'QUALIFY' ||
    normalized === 'REVIEW' ||
    normalized === 'WARNING'
  ) {
    badgeClass = 'badge-partial';
    IconComponent = AlertTriangle;
  } else if (
    normalized === 'NOT_VERIFIED' ||
    normalized === 'FAILED' ||
    normalized === 'INCORRECT' ||
    normalized === 'REJECT' ||
    normalized === 'ERROR' ||
    normalized === 'RISK_DETECTED'
  ) {
    badgeClass = 'badge-unverified';
    IconComponent = XCircle;
  } else if (normalized === 'TIMEOUT') {
    badgeClass = 'badge-partial';
    IconComponent = Clock;
  }

  return (
    <span className={`badge ${badgeClass}`}>
      {showIcon && <IconComponent size={13} strokeWidth={2.5} />}
      <span>{displayLabel}</span>
      {confidence !== null && confidence !== undefined && (
        <span
          style={{
            marginLeft: '0.25rem',
            paddingLeft: '0.35rem',
            borderLeft: '1px solid currentColor',
            opacity: 0.85,
            fontSize: '0.72rem',
          }}
        >
          {Math.round(confidence > 1 ? confidence : confidence * 100)}%
        </span>
      )}
    </span>
  );
}
