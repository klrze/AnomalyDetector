import { useState, useEffect } from 'react';
import { fetchEvaluationsByChannel, fetchExperimentsByChannel, fetchBestExperimentByChannel } from '../service/api';

function Data() {
  const [evaluations, setEvaluations] = useState([]);
  const [experiments, setExperiments] = useState([]);
  const [channel, setChannel] = useState('A-1');
  const [loading, setLoading] = useState(false);
  const [bestTrial, setBestTrial] = useState({});

  useEffect(() => {
    loadData();
  }, [channel]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [evalData, expData, bestData] = await Promise.all([
        fetchEvaluationsByChannel(channel),
        fetchExperimentsByChannel(channel),
        fetchBestExperimentByChannel(channel)
      ]);
      
      setEvaluations(evalData);
      setExperiments(expData);
      setBestTrial(bestData);
      
    } catch (error) {
      console.error("Error loading data:", error);
    } finally {
      setLoading(false);
    }
  };

  // Grab the single evaluation summary for this channel (if it exists)
  const currentEval = evaluations[0] || {};

  return (
    <div className="max-w-4xl mx-auto p-8 space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-blue-400">Telemetry Evaluation & Experiment History</h1>
      </div>

      {/* Channel Switcher Section */}
      <div className="space-y-3 text-left">
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Channels</h2>
        <div className="flex justify-start gap-4">
          {['A-1', 'B-1', 'C-1', 'T-1'].map((ch) => (
            <button
              key={ch}
              onClick={() => setChannel(ch)}
              className={`px-6 py-2 rounded-lg font-bold transition ${
                channel === ch 
                  ? 'bg-blue-600 text-white ring-2 ring-blue-400 ring-offset-2 ring-offset-slate-900' 
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {ch}
            </button>
          ))}
        </div>
      </div>


      {loading ? (
        <p className="text-slate-400 text-center py-12">Loading telemetry data from Spring Boot...</p>
      ) : (
        <>
          {/* 1. Final Evaluation Summary (Shown ONCE per channel) */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl space-y-3">
  <h2 className="text-lg font-semibold text-slate-200">Final Evaluation Summary</h2>
  <div className="flex justify-between items-center text-sm">
    <div>
      <span className="text-slate-400">Amount Flagged: </span>
      <span className="text-emerald-400 font-mono font-semibold">
        {currentEval.amountFlagged ?? 'N/A'}
      </span>
    </div>
    <div className="text-right text-slate-300 space-x-4">
      <span>Precision: <span className="font-mono text-slate-200">
        {currentEval.precision ?? 'N/A'}</span>
      </span>
      <span>Recall: <span className="font-mono text-slate-200">
        {currentEval.recall ?? 'N/A'}</span>
      </span>
      <span>F1 Score: <span className="font-mono text-blue-400 font-semibold">
        {currentEval.f1Score ?? currentEval.f1_score ?? 'N/A'}</span>
      </span>
    </div>
  </div>
            {/* Best Training Trial Section */}
          <div className="border-t border-slate-700/60 pt-3 mt-3 space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Training Performance</span>
              <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                ★ Best Training Trial
              </span>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
              <div className="bg-slate-900/50 p-2 rounded border border-slate-700/40">
                <span className="text-slate-400">Train Loss</span>
                <p className="font-mono font-bold text-slate-200 text-sm mt-0.5">{bestTrial?.finalTrainLoss?.toFixed(4) ?? 'N/A'}</p>
              </div>
              <div className="bg-slate-900/50 p-2 rounded border border-slate-700/40">
                <span className="text-slate-400">Val Loss</span>
                <p className="font-mono font-bold text-blue-400 text-sm mt-0.5">{bestTrial?.valLoss?.toFixed(4) ?? 'N/A'}</p>
              </div>
              <div className="bg-slate-900/50 p-2 rounded border border-slate-700/40">
                <span className="text-slate-400">Epochs</span>
                <p className="font-mono font-bold text-slate-200 text-sm mt-0.5">{bestTrial?.epochs ?? 'N/A'}</p>
              </div>
              <div className="bg-slate-900/50 p-2 rounded border border-slate-700/40">
                <span className="text-slate-400">Learning Rate</span>
                <p className="font-mono font-bold text-slate-200 text-sm mt-0.5">{bestTrial?.learningRate ?? 'N/A'}</p>
              </div>
            </div>
          </div>
          </div>

          {/* 2. Experiment Trial History (Multiple trials listed out) */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl space-y-6">
            <h2 className="text-lg font-semibold text-slate-200">Experiment Tuning History</h2>
            
            {experiments.length === 0 ? (
              <p className="text-slate-400">No experiment logs found for this channel.</p>
            ) : (
              <div className="space-y-4">
                {experiments.map((expLog, index) => {
                  // Fallback check for val loss field variations
                  const valLossValue = expLog.finalValLoss ?? expLog.valLoss ?? expLog.final_val_loss;

                  return (
                    <div 
                      key={expLog.id || index} 
                      className="bg-slate-900/60 border border-slate-700 p-5 rounded-xl space-y-3 shadow-md"
                    >
                      {/* Trial Number Header */}
                      <div className="flex justify-between items-center border-b border-slate-700 pb-2">
                        <span className="px-3 py-1 bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-full text-xs font-bold tracking-wide uppercase">
                          Trial #{index + 1}
                        </span>
                      </div>

                      {/* Experiment Configuration Grid */}
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm pt-2">
                        <div>
                          <span className="block text-slate-500 text-xs">Learning Rate</span>
                          <span className="text-slate-200 font-mono">{expLog.learningRate ?? 'N/A'}</span>
                        </div>
                        <div>
                          <span className="block text-slate-500 text-xs">Epochs</span>
                          <span className="text-slate-200 font-mono">{expLog.epochs ?? 'N/A'}</span>
                        </div>
                        <div>
                          <span className="block text-slate-500 text-xs">Train Loss</span>
                          <span className="text-slate-200 font-mono">{expLog.finalTrainLoss ?? 'N/A'}</span>
                        </div>
                        <div>
                          <span className="block text-slate-500 text-xs">Val Loss</span>
                          <span className="text-slate-200 font-mono">
                            {valLossValue !== undefined && valLossValue !== null ? valLossValue : 'N/A'}
                          </span>
                        </div>
                      </div>

                      {expLog.notes && (
                      <div className="pt-2 border-t border-slate-700/50 text-xs text-slate-300 italic text-left">
                        <span className="font-semibold text-slate-400 not-italic">Notes:</span> {expLog.notes}
                      </div>
                    )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default Data;