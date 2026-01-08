import { useState, useEffect } from 'react';
import { Check, Loader2 } from 'lucide-react';

const ThinkingProcess = ({ steps, isThinking }) => {
  const [visibleSteps, setVisibleSteps] = useState([]);

  useEffect(() => {
    if (!steps || steps.length === 0) return;

    // Animar steps progressivamente
    steps.forEach((step, index) => {
      setTimeout(() => {
        setVisibleSteps(prev => [...prev, step]);
      }, index * 300);
    });
  }, [steps]);

  if (!isThinking && (!steps || steps.length === 0)) return null;

  return (
    <div className="mb-4 p-4 bg-cerberus-darker border border-cerberus-border rounded-xl">
      <div className="flex items-center gap-2 mb-3">
        <Loader2 className={`w-4 h-4 text-blue-400 ${isThinking ? 'animate-spin' : ''}`} />
        <span className="text-sm font-medium text-cerberus-text-secondary">
          {isThinking ? 'Pensando...' : 'Processo de raciocínio'}
        </span>
      </div>
      
      <div className="space-y-2">
        {visibleSteps.map((step, index) => (
          <div
            key={index}
            className="flex items-start gap-3 animate-fade-in"
          >
            <div className={`mt-0.5 w-5 h-5 rounded-full flex items-center justify-center shrink-0 ${
              step.status === 'completed'
                ? 'bg-green-500/20 text-green-400'
                : 'bg-blue-500/20 text-blue-400'
            }`}>
              {step.status === 'completed' ? (
                <Check className="w-3 h-3" />
              ) : (
                <Loader2 className="w-3 h-3 animate-spin" />
              )}
            </div>
            <div className="flex-1">
              <div className="text-sm text-white font-medium">{step.step}</div>
              <div className="text-xs text-cerberus-text-muted">{step.description}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ThinkingProcess;
