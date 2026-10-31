function Home() {
  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-4xl font-bold text-blue-400 mb-4">NASA Telemetry Dashboard</h1>
      <p className="text-slate-300 mb-6 text-lg">
        Welcome to your local full-stack anomaly detection workspace (Spring Boot + Vite + React).
      </p>
      <a 
        href="/data" 
        className="inline-block bg-blue-600 px-6 py-3 rounded-lg text-white font-medium hover:bg-blue-500 transition shadow-lg"
      >
        View Telemetry Data →
      </a>
    </div>
  );
}

export default Home;