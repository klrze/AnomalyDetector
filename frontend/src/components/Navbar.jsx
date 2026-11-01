import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-slate-800 border-b border-slate-700 px-8 py-4 flex justify-center items-center shadow-md">
      {/* Navigation Button Boxes */}
      <div className="flex items-center gap-6 font-medium">
        <Link 
          to="/" 
          className="px-5 py-2 rounded-lg bg-slate-700 text-slate-200 hover:bg-slate-600 hover:text-white transition shadow"
        >
          Overview
        </Link>
        <Link 
          to="/data" 
          className="px-5 py-2 rounded-lg bg-slate-700 text-slate-200 hover:bg-slate-600 hover:text-white transition shadow"
        >
          Data 
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;