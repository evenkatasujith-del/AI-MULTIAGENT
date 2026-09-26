import React from 'react';
import { AlertCircle, RefreshCw, X } from 'lucide-react';

export default function ErrorBanner({ error, onRetry, onDismiss }) {
  if (!error) return null;

  return (
    <div
      style={{
        background: '#fef2f2',
        border: '1px solid #fecaca',
        borderRadius: 'var(--radius-lg)',
        padding: '1.25rem 1.5rem',
        marginBottom: '1.5rem',
        display: 'flex',
        alignItems: 'flex-start',
        gap: '1rem',
      }}
    >
      <AlertCircle size={22} color="#dc2626" style={{ flexShrink: 0, marginTop: '2px' }} />

      <div style={{ flex: 1 }}>
        <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#991b1b' }}>
          Verification Error
        </h4>
        <p style={{ fontSize: '0.875rem', color: '#b91c1c', marginTop: '0.25rem', lineHeight: 1.5 }}>
          {error}
        </p>

        {onRetry && (
          <div style={{ marginTop: '0.75rem' }}>
            <button
              type="button"
              className="btn-secondary"
              onClick={onRetry}
              style={{
                fontSize: '0.8rem',
                padding: '0.35rem 0.75rem',
                borderColor: '#fca5a5',
                color: '#991b1b',
              }}
            >
              <RefreshCw size={13} />
              <span>Try Again</span>
            </button>
          </div>
        )}
      </div>

      {onDismiss && (
        <button
          type="button"
          onClick={onDismiss}
          style={{
            background: 'transparent',
            border: 'none',
            color: '#dc2626',
            cursor: 'pointer',
            padding: '4px',
          }}
          title="Dismiss"
        >
          <X size={18} />
        </button>
      )}
    </div>
  );
}
