function Home() {
  return (
    <div className="max-w-4xl mx-auto p-8 space-y-6">
      <h1 className="text-6xl font-bold text-blue-400 mb-4">Anomaly Telemetry Detector</h1>
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

      {/* Tech Stack & Data Source Section */}
      <div className="space-y-4 pt-4">
        {/* Standalone Heading Out of the Box */}
        <h2 className="text-2xl font-bold text-blue-400 uppercase tracking-widest text-center">
          Tech Stack
        </h2>
        
        {/* The Box */}
        <div className="bg-slate-800/60 border border-slate-700/60 p-8 rounded-xl shadow-lg">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-8 gap-x-4 text-center">
            
            {/* Row 1 */}
            <div>
              <h3 className="text-lg font-bold text-slate-200 uppercase tracking-wide">Languages</h3>
              <p className="text-blue-300/80 font-mono text-base mt-1">Python, Java, JavaScript</p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-200 uppercase tracking-wide">Database</h3>
              <p className="text-blue-300/80 font-mono text-base mt-1">PostgreSQL</p>
            </div>

            {/* Row 2 */}
            <div>
              <h3 className="text-lg font-bold text-slate-200 uppercase tracking-wide">Frameworks</h3>
              <p className="text-blue-300/80 font-mono text-base mt-1">Spring Boot</p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-200 uppercase tracking-wide">IDE</h3>
              <p className="text-blue-300/80 font-mono text-base mt-1">Visual Studio Code</p>
            </div>

            {/* Row 3 */}
            <div>
              <h3 className="text-lg font-bold text-slate-200 uppercase tracking-wide">Libraries</h3>
              <p className="text-blue-300/80 font-mono text-base mt-1">PyTorch, NumPy, Pandas, Matplotlib, Hibernate</p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-200 uppercase tracking-wide">Dataset</h3>
              <p className="mt-1">
                <a 
                  href="https://www.kaggle.com/datasets/patrickfleith/nasa-anomaly-detection-dataset-smap-msl/data" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="text-blue-400 hover:text-blue-300 hover:underline font-mono text-base"
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