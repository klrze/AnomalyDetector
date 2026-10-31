import { useState, useEffect } from 'react';
import { fetchEvaluationsByChannel } from '../service/api';

function Data() {
  const [evaluations, setEvaluations] = useState([]);
  const [channel, setChannel] = useState('A-1');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, [channel]);

  const loadData = async () => {
    setLoading(true);
    const data = await fetchEvaluationsByChannel(channel);
    setEvaluations(data);
    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-blue-400">Telemetry Evaluation Logs</h1>
        <a href="/" className="text-slate-400 hover:text-white underline">← Back to Home</a>
      </div>

      {/* Channel Switcher Buttons */}
      <div className="flex gap-4 mb-6">
        {['A-1', 'B-1'].map((ch) => (
          <button
            key={ch}
            onClick={() => setChannel(ch)}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              channel === ch ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Channel {ch}
          </button>
        ))}
      </div>

      {/* Data Container Card */}
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl">
        <h2 className="text-lg font-semibold mb-4 text-slate-200">Logs for Channel: {channel}</h2>
        
        {loading ? (
          <p className="text-slate-400">Loading telemetry data from Spring Boot...</p>
        ) : evaluations.length === 0 ? (
          <p className="text-slate-400">No logs found for this channel.</p>
        ) : (
          <div className="space-y-4">
            {evaluations.map((evalLog) => (
              <div 
                key={evalLog.id} 
                className="bg-slate-900/50 border border-slate-700/50 p-4 rounded-lg flex justify-between items-center"
              >
                <div>
                  <p className="text-sm text-slate-400">Record ID: {evalLog.id}</p>
                  <p className="text-emerald-400 font-mono">Flagged Count: {evalLog.amountFlagged}</p>
                </div>
                <div className="text-right text-sm text-slate-300">
                  <p>Precision: {evalLog.precision}</p>
                  <p>Recall: {evalLog.recall}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Data;