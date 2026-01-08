import { Square } from 'lucide-react';

const StopButton = ({ onStop, loading }) => {
  if (!loading) return null;

  return (
    <div className="flex justify-center mb-4">
      <button
        onClick={onStop}
        className="flex items-center gap-2 px-4 py-2 bg-red-500/20 text-red-400 border border-red-500/30 rounded-lg hover:bg-red-500/30 transition-colors text-sm font-medium"
      >
        <Square className="w-4 h-4 fill-current" />
        Parar Geração
      </button>
    </div>
  );
};

export default StopButton;
