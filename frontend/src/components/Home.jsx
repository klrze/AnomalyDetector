function Home() {
  return (
    <div className="max-w-4xl mx-auto p-8 space-y-6">
      <h1 className="text-4xl font-bold text-blue-400 mb-4">Anomaly Telemetry Detector</h1>
      <p className="text-slate-300 mb-6 text-lg">
        By: Klarizze Martinez
      </p>
      
      {/* Project Overview */}
      <p className="text-slate-300 text-base leading-relaxed bg-slate-800/60 border border-slate-700/60 p-6 rounded-xl shadow-lg">
        A full-stack anomaly detection pipeline built to monitor critical spacecraft telemetry channels. 
        Sequential time-series data is processed using a custom PyTorch multi-layer perceptron via sliding-window analysis, flagging anomalies through dynamic residual Mean Squared Error (MSE) thresholds. 
        Data pipeline management and PostgreSQL persistence are driven by Python, while a Java Spring Boot backend serves 
        experiment metrics and evaluation history to the React frontend.
      </p>

      {/* Tech Stack & Data Source */}
      <div className="bg-slate-800/60 border border-slate-700/60 p-6 rounded-xl shadow-lg space-y-4">
        <h2 className="text-xs font-bold uppercase tracking-wider text-blue-400">Tech Stack & Data Source</h2>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm text-slate-300">
          <div className="space-y-3">
            <div>
              <h3 className="font-bold text-blue-300 text-xs uppercase tracking-wide">Languages</h3>
              <p className="text-slate-400 font-mono text-xs mt-1">Python, Java, JavaScript</p>
            </div>

            <div>
              <h3 className="font-bold text-blue-300 text-xs uppercase tracking-wide">Frameworks</h3>
              <p className="text-slate-400 font-mono text-xs mt-1">Spring Boot</p>
            </div>

            <div>
              <h3 className="font-bold text-blue-300 text-xs uppercase tracking-wide">Libraries</h3>
              <p className="text-slate-400 font-mono text-xs mt-1">PyTorch, NumPy, Pandas, Matplotlib, Hibernate</p>
            </div>
          </div>

          <div className="space-y-3">
            <div>
              <h3 className="font-bold text-blue-300 text-xs uppercase tracking-wide">Database</h3>
              <p className="text-slate-400 font-mono text-xs mt-1">PostgreSQL</p>
            </div>

            <div>
              <h3 className="font-bold text-blue-300 text-xs uppercase tracking-wide">IDE</h3>
              <p className="text-slate-400 font-mono text-xs mt-1">Visual Studio Code</p>
            </div>

            <div>
              <h3 className="font-bold text-blue-300 text-xs uppercase tracking-wide">Dataset</h3>
              <p className="text-xs mt-1">
                <a 
                  href="https://www.kaggle.com/datasets/patrickfleith/nasa-anomaly-detection-dataset-smap-msl/data" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="text-blue-400 hover:underline font-mono"
                >
                  NASA Anomaly Detection Dataset (Kaggle)
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
      
    </div>
  );
}

export default Home;