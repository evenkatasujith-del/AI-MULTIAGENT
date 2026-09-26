import React, { useEffect, useState } from 'react';
import { ShieldCheck, BookOpen, History, Activity, Sparkles } from 'lucide-react';
import { checkBackendHealth } from '../api';

export default function Navbar({ activeTab, setActiveTab, historyCount = 0 }) {
  const [backendStatus, setBackendStatus] = useState({ checked: false, online: false });

  const verifyHealth = async () => {
    const status = await checkBackendHealth();
    setBackendStatus({ checked: true, online: status.online });
  };

  useEffect(() => {
    verifyHealth();
    const interval = setInterval(verifyHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="header-nav">
      <div className="header-inner">
        <div className="brand" onClick={() => setActiveTab('home')}>
          <div className="brand-icon-wrap">
            <ShieldCheck size={22} strokeWidth={2.5} />
          </div>
          <div>
            <div className="brand-title">
              Verify<span>AI</span>
            </div>
          </div>
        </div>

        <nav className="nav-links">
          <button
            type="button"
            className={`nav-link ${activeTab === 'home' ? 'active' : ''}`}
            onClick={() => setActiveTab('home')}
          >
            <Sparkles size={16} />
            <span>Verify</span>
          </button>

          <button
            type="button"
            className={`nav-link ${activeTab === 'how-it-works' ? 'active' : ''}`}
            onClick={() => setActiveTab('how-it-works')}
          >
            <BookOpen size={16} />
            <span>How It Works</span>
          </button>

          <button
            type="button"
            className={`nav-link ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            <History size={16} />
            <span>History</span>
            {historyCount > 0 && (
              <span
                style={{
                  background: 'var(--primary-100)',
                  color: 'var(--primary-800)',
                  fontSize: '0.7rem',
                  fontWeight: 700,
                  padding: '0.1rem 0.4rem',
                  borderRadius: '999px',
                }}
              >
                {historyCount}
              </span>
            )}
          </button>

          <div
            className="status-pill"
            title={
              backendStatus.checked
                ? backendStatus.online
                  ? 'FastAPI Backend Connected (127.0.0.1:8000)'
                  : 'FastAPI Backend Disconnected'
                : 'Checking server connection...'
            }
          >
            <span
              className={`status-dot ${
                backendStatus.checked ? (backendStatus.online ? 'online' : 'offline') : ''
              }`}
            />
            <span style={{ color: 'var(--text-subtle)' }}>
              {backendStatus.checked ? (backendStatus.online ? 'Backend Live' : 'Offline') : 'Checking...'}
            </span>
          </div>
        </nav>
      </div>
    </header>
  );
}
