import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MapPin, Users, Activity, Filter, Search } from 'lucide-react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import ParticleBackground from '../components/ParticleBackground';
import { getCities } from '../services/api';

const CitiesPage = () => {
    const [cities, setCities] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filterRisk, setFilterRisk] = useState('All');

    useEffect(() => {
        const fetchCities = async () => {
            try {
                const data = await getCities();
                setCities(data);
            } catch (error) {
                console.error("Failed to load cities", error);
                setError("Failed to connect to backend API.");
            } finally {
                setLoading(false);
            }
        };
        fetchCities();
    }, []);

    const filteredCities = cities.filter(city => {
        if (filterRisk === 'All') return true;
        return city.current_risk === filterRisk;
    });

    return (
        <div className="relative min-h-screen bg-slate-950 font-sans text-white selection:bg-cyan-500/30 selection:text-cyan-200">
            <ParticleBackground />
            <Navbar />

            <div className="relative z-10 pt-32 pb-20 px-6 max-w-7xl mx-auto">

                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="mb-12"
                >
                    <div className="flex items-center gap-2 text-cyan-400 mb-4 font-medium">
                        <MapPin className="w-5 h-5" />
                        <span>City Explorer</span>
                    </div>
                    <h1 className="text-5xl md:text-6xl font-bold mb-6">Choose Your City</h1>
                    <p className="text-slate-400 text-lg max-w-2xl leading-relaxed">
                        Select a city to explore its urban data story. Each city reveals unique patterns in weather, air quality, traffic, and health.
                    </p>
                </motion.div>

                {/* Filters */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.1 }}
                    className="flex flex-wrap items-center gap-4 mb-12"
                >
                    <div className="flex items-center gap-2 text-slate-500 mr-4">
                        <Filter className="w-4 h-4" />
                        <span className="text-sm font-medium">Filter by risk:</span>
                    </div>

                    {['All', 'Low', 'Medium', 'High'].map((filter, i) => (
                        <button
                            key={filter}
                            onClick={() => setFilterRisk(filter)}
                            className={`px-6 py-2 rounded-full text-sm font-medium transition-all ${filterRisk === filter
                                ? 'bg-cyan-400 text-slate-950 shadow-[0_0_15px_rgba(34,211,238,0.3)]'
                                : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white'
                                }`}
                        >
                            {filter}
                        </button>
                    ))}
                </motion.div>

                {/* Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-20">
                    {loading ? (
                        <div className="text-white text-center col-span-full">Loading cities...</div>
                    ) : error ? (
                        <div className="text-red-400 text-center col-span-full bg-red-900/20 p-4 rounded-lg border border-red-500/50">
                            <p className="font-bold">Error Loading Data</p>
                            <p className="text-sm">{error}</p>
                        </div>
                    ) : filteredCities.length === 0 ? (
                        <div className="text-slate-500 text-center col-span-full py-12">No cities found with {filterRisk} risk.</div>
                    ) : filteredCities.map((city, index) => (
                        <Link
                            to={`/dashboard/${city.city_id}`}
                            key={index}
                        >
                            <motion.div
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ duration: 0.5, delay: index * 0.1 }}
                                className="bg-slate-900/40 border border-slate-800 rounded-2xl p-6 group hover:border-slate-700 hover:bg-slate-900/60 transition-all cursor-pointer h-full"
                            >
                                <div className="flex justify-between items-start mb-8">
                                    <div className="flex items-center gap-2 text-slate-500">
                                        <MapPin className="w-4 h-4" />
                                        <span className="text-sm">{city.state}</span>
                                    </div>
                                    <span className={`px-3 py-1 rounded-full text-xs font-bold text-white bg-slate-700 group-hover:bg-cyan-600 transition-colors`}>
                                        View Data
                                    </span>
                                </div>

                                <h3 className="text-3xl font-bold mb-2 group-hover:text-cyan-400 transition-colors">{city.city_name}</h3>

                                <div className="flex items-center gap-6 text-slate-400 text-sm font-medium mb-6">
                                    <div className="flex items-center gap-1.5">
                                        <Users className="w-4 h-4" />
                                        <span className={`${city.current_risk === 'High' ? 'text-rose-400' : city.current_risk === 'Medium' ? 'text-amber-400' : 'text-emerald-400'}`}>
                                            Risk: {city.current_risk}
                                        </span>
                                    </div>
                                    <div className="flex items-center gap-1.5 text-cyan-400">
                                        <Activity className="w-4 h-4" />
                                        Live
                                    </div>
                                </div>

                                <div className="text-xs text-slate-600 font-mono">
                                    {city.latitude && city.longitude ? `${Number(city.latitude).toFixed(2)}°N, ${Number(city.longitude).toFixed(2)}°W` : ''}
                                </div>
                            </motion.div>
                        </Link>
                    ))}
                </div>

            </div>

            {/* Stats Footer */}
            <div className="bg-slate-900 border-t border-slate-800 py-10 relative z-20">
                <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
                    {[
                        { val: "6", label: "Cities Monitored", color: "text-cyan-400" },
                        { val: "24/7", label: "Live Monitoring", color: "text-blue-400" },
                        { val: "5", label: "Data Domains", color: "text-emerald-400" },
                        { val: "1M+", label: "Data Points", color: "text-rose-400" }
                    ].map((stat, i) => (
                        <div key={i}>
                            <div className={`text-4xl md:text-5xl font-bold mb-2 ${stat.color}`}>{stat.val}</div>
                            <div className="text-slate-400 text-sm uppercase tracking-wider">{stat.label}</div>
                        </div>
                    ))}
                </div>
            </div>

        </div>
    );
};

export default CitiesPage;
