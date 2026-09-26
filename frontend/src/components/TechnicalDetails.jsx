import React, { useState } from 'react';
import { ChevronDown, Code2, Copy, Check } from 'lucide-react';

export default function TechnicalDetails({ data }) {
  const [open, setOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!data) return null;

  const jsonString = JSON.stringify(data, null, 2);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(jsonString);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
    }
  };

  return (
    <div className="tech-details-wrap">
      <button
        type="button"
        className="tech-details-trigger"
        onClick={() => setOpen(!open)}
      >
        <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Code2 size={16} color="var(--primary-600)" />
          <span>View Technical Details (Raw Backend JSON)</span>
        </span>
        <ChevronDown
          size={18}
          className={`expand-chevron ${open ? 'open' : ''}`}
        />
      </button>

      {open && (
        <div className="tech-details-body">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.65rem' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-subtle)' }}>
              Unified endpoint response from <code>POST /smart-verify</code>
            </span>
            <button
              type="button"
              className="btn-secondary"
              style={{ padding: '0.3rem 0.65rem', fontSize: '0.75rem' }}
              onClick={handleCopy}
            >
              {copied ? (
                <>
                  <Check size={12} color="var(--primary-600)" />
                  <span>Copied JSON</span>
                </>
              ) : (
                <>
                  <Copy size={12} />
                  <span>Copy JSON</span>
                </>
              )}
            </button>
          </div>

          <pre className="json-viewer">
            <code>{jsonString}</code>
          </pre>
        </div>
      )}
    </div>
  );
}
