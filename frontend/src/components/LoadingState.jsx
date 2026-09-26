import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2, Sparkles, BrainCircuit } from 'lucide-react';

const STEPS = [
  { id: 1, label: 'Analyzing user question & intent' },
  { id: 2, label: 'Detecting question type (FACT / MATH / CODE)' },
  { id: 3, label: 'Generating primary AI response' },
  { id: 4, label: 'Retrieving ground truth evidence & sandbox execution' },
  { id: 5, label: 'Synthesizing dual-verification signals & final decision' },
];

export default function LoadingState() {
  const [currentStep, setCurrentStep] = useState(1);

  useEffect(() => {
    const timer1 = setTimeout(() => setCurrentStep(2), 1200);
    const timer2 = setTimeout(() => setCurrentStep(3), 2800);
    const timer3 = setTimeout(() => setCurrentStep(4), 5000);
    const timer4 = setTimeout(() => setCurrentStep(5), 7500);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
      clearTimeout(timer4);
    };
  }, []);

  return (
    <div className="loading-card">
      <div className="loading-spinner-wrap">
        <div className="loading-spinner" />
        <div className="loading-pulse-core">
          <BrainCircuit size={16} />
        </div>
      </div>

      <h3 className="loading-headline">Verifying Your Question...</h3>
      <p className="loading-subtext">
        Multi-agent verification pipeline is actively inspecting claims, calculation, or code.
      </p>

      <div className="loading-steps">
        {STEPS.map((step) => {
          const isDone = currentStep > step.id;
          const isActive = currentStep === step.id;

          return (
            <div
              key={step.id}
              className={`loading-step ${isActive ? 'active' : ''} ${isDone ? 'completed' : ''}`}
            >
              <div className="step-icon">
                {isDone ? (
                  <CheckCircle2 size={18} color="var(--primary-600)" />
                ) : isActive ? (
                  <Loader2 size={18} color="var(--primary-600)" className="loading-spinner" style={{ width: 18, height: 18, borderWidth: 2 }} />
                ) : (
                  <div
                    style={{
                      width: 10,
                      height: 10,
                      borderRadius: '50%',
                      background: 'var(--border-medium)',
                    }}
                  />
                )}
              </div>

              <span>{step.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
