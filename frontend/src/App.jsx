import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Data from './components/Data';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-900 text-white font-sans">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/data" element={<Data />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;