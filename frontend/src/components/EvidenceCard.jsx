import React from 'react';
import { ExternalLink, BookOpen, AlertCircle } from 'lucide-react';

export default function EvidenceCard({ source }) {
  if (!source) return null;

  const relevancePct = source.relevance
    ? Math.round(source.relevance > 1 ? source.relevance : source.relevance * 100)
    : null;

  return (
    <div className="evidence-card">
      <div className="evidence-card-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <BookOpen size={16} color="var(--primary-600)" />
          <h4 className="evidence-title">{source.title || 'Untitled Source'}</h4>
        </div>
        {relevancePct !== null && (
          <span className="relevance-tag" title="Relevance match to claim">
            {relevancePct}% Match
          </span>
        )}
      </div>

      <p className="evidence-snippet">
        {source.evidence || 'No text snippet available.'}
      </p>

      <div className="evidence-footer">
        <span style={{ fontSize: '0.75rem', color: 'var(--text-light)' }}>
          Wikipedia Grounding
        </span>
        {source.url ? (
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="open-source-link"
          >
            <span>Open Source</span>
            <ExternalLink size={13} />
          </a>
        ) : (
          <span style={{ fontSize: '0.75rem', color: 'var(--text-subtle)' }}>No URL</span>
        )}
      </div>
    </div>
  );
}

export function InsufficientEvidenceNotice({ message }) {
  return (
    <div
      style={{
        background: '#fffbeb',
        border: '1px solid #fde68a',
        borderRadius: 'var(--radius-md)',
        padding: '1rem 1.25rem',
        display: 'flex',
        alignItems: 'flex-start',
        gap: '0.75rem',
        marginTop: '0.5rem',
      }}
    >
      <AlertCircle size={20} color="#b45309" style={{ flexShrink: 0, marginTop: '2px' }} />
      <div>
        <div style={{ fontWeight: 700, color: '#92400e', fontSize: '0.9rem' }}>
          Insufficient Evidence
        </div>
        <p style={{ color: '#b45309', fontSize: '0.85rem', marginTop: '0.2rem', lineHeight: 1.5 }}>
          {message || 'VerifyAI could not find enough reliable evidence to verify this claim.'}
        </p>
      </div>
    </div>
  );
}
