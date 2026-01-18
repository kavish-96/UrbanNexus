import { motion } from 'framer-motion';
import { Activity } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();
    const isActive = (path) => {
        if (path === '/dashboard') return location.pathname.startsWith('/dashboard');
        return location.pathname === path;
    };

    return (
        <motion.nav
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6 }}
            className="fixed top-0 left-0 right-0 z-50 px-6 py-4 flex items-center justify-between max-w-7xl mx-auto"
        >
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2">
                <div className="w-8 h-8 bg-slate-800 rounded-lg flex items-center justify-center text-cyan-400">
                    <Activity className="w-5 h-5" />
                </div>
                <span className="text-xl font-bold text-white tracking-tight">UrbanNexus</span>
            </Link>

            {/* Navigation Pills */}
            <div className="hidden md:flex items-center bg-slate-900/50 backdrop-blur-md rounded-full p-1 border border-slate-800">
                <Link
                    to="/"
                    className={`flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium transition-all ${isActive('/') ? 'bg-slate-800/80 text-cyan-400 shadow-sm' : 'text-slate-400 hover:text-white'}`}
                >
                    <Activity className={`w-3.5 h-3.5 ${isActive('/') ? 'opacity-100' : 'opacity-0 hidden'}`} />
                    Home
                </Link>
                <Link
                    to="/cities"
                    className={`px-5 py-1.5 rounded-full text-sm font-medium transition-all ${isActive('/cities') ? 'bg-slate-800/80 text-cyan-400 shadow-sm' : 'text-slate-400 hover:text-white'}`}
                >
                    Cities
                </Link>
                <Link
                    to="/dashboard/2"
                    className={`px-5 py-1.5 rounded-full text-sm font-medium transition-all ${isActive('/dashboard') ? 'bg-slate-800/80 text-cyan-400 shadow-sm' : 'text-slate-400 hover:text-white'}`}
                >
                    Dashboard
                </Link>
                <Link
                    to="/simulation"
                    className={`px-5 py-1.5 rounded-full text-sm font-medium transition-all ${isActive('/simulation') ? 'bg-slate-800/80 text-cyan-400 shadow-sm' : 'text-slate-400 hover:text-white'}`}
                >
                    Simulation
                </Link>
            </div>

            {/* CTA */}
            <Link
                to="/cities"
                className="hidden md:block px-5 py-2 bg-cyan-400 hover:bg-cyan-300 text-slate-900 rounded-md text-sm font-bold shadow-[0_0_15px_rgba(34,211,238,0.3)] transition-all transform hover:scale-105"
            >
                Explore Cities
            </Link>
        </motion.nav>
    );
};

export default Navbar;
