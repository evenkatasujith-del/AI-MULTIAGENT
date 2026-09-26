import React from 'react';
import { History, Trash2, ArrowRight, Clock, HelpCircle, Layers } from 'lucide-react';
import StatusBadge from './StatusBadge';

export default function HistoryView({
  historyItems = [],
  onSelectHistoryItem,
  onClearHistory,
  onBackToDashboard,
}) {
  if (historyItems.length === 0) {
    return (
      <div className="history-container">
        <div className="history-header">
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-main)' }}>
            Verification History
          </h2>
        </div>

        <div
          className="loading-card"
          style={{ padding: '3.5rem 2rem', borderColor: 'var(--border-default)' }}
        >
          <div
            style={{
              width: 56,
              height: 56,
              borderRadius: '50%',
              background: 'var(--bg-card-subtle)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 1rem',
              color: 'var(--text-light)',
            }}
          >
            <History size={26} />
          </div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.4rem' }}>
            No History Yet
          </h3>
          <p style={{ color: 'var(--text-subtle)', fontSize: '0.9rem', maxWidth: '420px', margin: '0 auto 1.5rem' }}>
            Questions you verify are stored in your browser's local storage so you can easily review previous claims, math calculations, and code executions.
          </p>
          <button
            type="button"
            className="btn-primary"
            onClick={onBackToDashboard}
          >
            <span>Ask Your First Question</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-main)' }}>
            Verification History
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-subtle)' }}>
            {historyItems.length} saved {historyItems.length === 1 ? 'verification' : 'verifications'} (stored locally)
          </p>
        </div>

        <button
          type="button"
          className="btn-secondary"
          onClick={onClearHistory}
          style={{ color: '#b91c1c' }}
        >
          <Trash2 size={14} />
          <span>Clear History</span>
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {historyItems.map((item) => {
          const type = item.type || 'FACT';
          const typeClass = type.toLowerCase();
          const timestamp = item.timestamp
            ? new Date(item.timestamp).toLocaleString(undefined, {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
              })
            : '';

          return (
            <div
              key={item.id}
              className="history-card"
              onClick={() => onSelectHistoryItem(item)}
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.45rem', flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                  <span className={`example-tag ${typeClass}`}>{type}</span>
                  <StatusBadge status={item.status} confidence={item.confidence} />
                  {timestamp && (
                    <span
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.25rem',
                        fontSize: '0.75rem',
                        color: 'var(--text-light)',
                        marginLeft: 'auto',
                      }}
                    >
                      <Clock size={12} />
                      {timestamp}
                    </span>
                  )}
                </div>

                <div
                  style={{
                    fontSize: '1rem',
                    fontWeight: 600,
                    color: 'var(--text-main)',
                    lineHeight: 1.4,
                  }}
                >
                  {item.question}
                </div>
              </div>

              <div style={{ color: 'var(--primary-600)', display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.85rem', fontWeight: 600 }}>
                <span>View</span>
                <ArrowRight size={16} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
