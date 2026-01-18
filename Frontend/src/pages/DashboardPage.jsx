import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    ArrowLeft, Clock, Thermometer, Wind, Car, Droplets,
    Activity, Info, TrendingUp, Sprout, RefreshCw
} from 'lucide-react';
import Navbar from '../components/Navbar';
import ParticleBackground from '../components/ParticleBackground';
import { getDashboardData, syncLiveWeather } from '../services/api';

// --- Sub-components ---

const InteractiveSparkline = ({ data, color, height = 40 }) => {
    // Determine color class -> hex for SVG
    const getColorHex = (c) => {
        if (c.includes("sky")) return "#38bdf8";
        if (c.includes("emerald")) return "#34d399";
        if (c.includes("rose")) return "#fb7185";
        if (c.includes("purple")) return "#c084fc";
        if (c.includes("amber")) return "#fbbf24";
        if (c.includes("blue")) return "#60a5fa";
        return "#94a3b8"; // Slate-400
    };

    const stroke = getColorHex(color);
    const max = Math.max(...data) || 1;
    const min = Math.min(...data) || 0;
    const range = max - min || 1;

    // Normalize points
    const points = data.map((val, i) => {
        const x = (i / (data.length - 1)) * 100;
        const y = 100 - ((val - min) / range) * 100;
        return `${x},${y}`;
    }).join(" ");

    return (
        <div className={`w-full overflow-hidden`} style={{ height: `${height}px` }}>
            <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="w-full h-full overflow-visible">
                <motion.path
                    d={`M ${points}`}
                    fill="none"
                    stroke={stroke}
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    initial={{ pathLength: 0, opacity: 0 }}
                    animate={{ pathLength: 1, opacity: 1 }}
                    transition={{ duration: 1.5, ease: "easeInOut" }}
                />
            </svg>
        </div>
    );
};

const StatCard = ({ data }) => {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-slate-900/40 border border-slate-800 p-6 rounded-2xl backdrop-blur-sm relative overflow-hidden group hover:bg-slate-900/60 transition-colors"
        >
            <div className={`absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity ${data.color}`}>
                <data.icon size={64} />
            </div>

            <div className="relative z-10">
                <div className="flex justify-between items-start mb-4">
                    <div className={`p-2 rounded-lg ${data.bg} ${data.color}`}>
                        <data.icon size={20} />
                    </div>
                </div>

                <div className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-1">{data.label}</div>
                <div className="flex items-baseline gap-2 mb-4">
                    <span className="text-3xl font-bold text-white tracking-tight">{data.val}</span>
                    <span className={`text-sm font-medium items-center gap-1 ${data.trend === 'Good' ? 'text-emerald-400' : 'text-slate-500'}`}>
                        {data.unit}
                    </span>
                    {data.sub && <div className="text-xs text-slate-500 ml-2">{data.sub}</div>}
                </div>

                {/* Mini Chart */}
                <div className="h-10 w-24 opacity-60 group-hover:opacity-100 transition-opacity">
                    <InteractiveSparkline data={data.chartData} color={data.color} />
                </div>
            </div>
        </motion.div>
    );
};

const Gauge = ({ score }) => {
    // Score 0-100.
    const r = 40;
    const c = 2 * Math.PI * r;
    const offset = c - (score / 100) * c;

    return (
        <div className="relative w-40 h-40 flex items-center justify-center">
            {/* Background Circle */}
            <svg className="w-full h-full -rotate-90">
                <circle cx="50%" cy="50%" r={r} stroke="#1e293b" strokeWidth="8" fill="none" />
                <motion.circle
                    cx="50%"
                    cy="50%"
                    r={r}
                    stroke={score > 70 ? "#34d399" : score > 50 ? "#fbbf24" : "#fb7185"}
                    strokeWidth="8"
                    fill="none"
                    strokeDasharray={c}
                    strokeDashoffset={c} // Init
                    animate={{ strokeDashoffset: offset }}
                    transition={{ duration: 1.5, ease: "easeOut" }}
                    strokeLinecap="round"
                />
            </svg>
            <div className="absolute flex flex-col items-center">
                <span className="text-4xl font-bold text-white">{score}</span>
                <span className="text-xs text-slate-400 uppercase tracking-widest">Health</span>
            </div>
        </div>
    );
};

const DomainCard = ({ title, value, unit, color, icon: Icon, chartData }) => {
    return (
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl hover:border-slate-700 transition-colors">
            <div className="flex items-center gap-3 mb-4">
                <div className={`p-2 rounded-lg bg-slate-800 ${color}`}>
                    <Icon size={18} />
                </div>
                <span className="font-medium text-slate-300">{title}</span>
            </div>
            <div className="flex items-end justify-between">
                <div>
                    <span className="text-2xl font-bold text-white">{value}</span>
                    <span className="text-xs text-slate-500 ml-1">{unit}</span>
                </div>
                {chartData && (
                    <div className="w-16 h-8">
                        <InteractiveSparkline data={chartData} color={color} height={32} />
                    </div>
                )}
            </div>
        </div>
    );
};

const DashboardPage = () => {
    const { cityId } = useParams();
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isSyncing, setIsSyncing] = useState(false);

    // Function to calculate logical status labels
    const getStatus = (val, type) => {
        if (type === 'aqi') return val > 150 ? "Unhealthy" : val > 100 ? "Poor" : val > 50 ? "Moderate" : "Good";
        if (type === 'traffic') return val > 7 ? "Congested" : val > 4 ? "Moderate" : "Clear";
        if (type === 'temp') return val > 35 ? "Hot" : val < 10 ? "Cold" : "Pleasant";
        return "Normal";
    };

    const handleSync = async () => {
        setIsSyncing(true);
        try {
            await syncLiveWeather();
            // In a real app we would wait a moment or confirm
            alert("Live Weather Synced & Updated!");
            window.location.reload();
        } catch (err) {
            alert("Sync Failed: " + err.message);
        } finally {
            setIsSyncing(false);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const apiData = await getDashboardData(cityId);

                // Transform API data to Component format
                const stats = apiData.latest_stats;

                // Determine timestamps
                const weatherTime = stats.weather_updated_at ? new Date(stats.weather_updated_at).toLocaleString() : "N/A";

                const tempStatus = getStatus(stats.temperature, 'temp');
                const aqiStatus = getStatus(stats.aqi, 'aqi');
                const trafficStatus = getStatus(stats.traffic_density, 'traffic');

                const transformed = {
                    city: apiData.city,
                    lastUpdated: weatherTime,
                    temp: {
                        val: stats.temperature,
                        unit: "°C",
                        label: "Temperature",
                        sub: `Feels ${tempStatus}. Humidity is ${stats.humidity}%.`,
                        trend: tempStatus,
                        statusColor: tempStatus === 'Hot' ? 'border-rose-500/50 text-rose-400' : 'border-emerald-500/50 text-emerald-400',
                        color: "text-sky-400",
                        bg: "bg-sky-500/10",
                        icon: Thermometer,
                        chartData: [stats.temperature - 2, stats.temperature - 1, stats.temperature]
                    },
                    aqi: {
                        val: stats.aqi,
                        unit: "AQI",
                        label: "Air Quality",
                        trend: aqiStatus,
                        sub: `PM2.5 levels are contributing to ${aqiStatus.toLowerCase()} air.`,
                        statusColor: stats.aqi > 100 ? 'border-rose-500/50 text-rose-400' : 'border-emerald-500/50 text-emerald-400',
                        color: stats.aqi > 100 ? "text-rose-400" : "text-emerald-400",
                        bg: stats.aqi > 100 ? "bg-rose-500/10" : "bg-emerald-500/10",
                        icon: Wind,
                        chartData: [stats.aqi - 10, stats.aqi + 5, stats.aqi]
                    },
                    traffic: {
                        val: stats.traffic_density,
                        unit: "/ 10",
                        label: "Traffic Density",
                        sub: `Congestion Level: ${trafficStatus}`,
                        trend: trafficStatus,
                        statusColor: stats.traffic_density > 7 ? 'border-rose-500/50 text-rose-400' : 'border-emerald-500/50 text-emerald-400',
                        color: "text-purple-400",
                        bg: "bg-purple-500/10",
                        icon: Car,
                        chartData: [stats.traffic_density, stats.traffic_density, stats.traffic_density]
                    },
                    humidity: {
                        val: stats.humidity,
                        unit: "%",
                        label: "Humidity",
                        sub: "Relative humidity level",
                        trend: stats.humidity > 80 ? "High" : "Normal",
                        statusColor: "border-blue-500/50 text-blue-400",
                        color: "text-blue-400",
                        bg: "bg-blue-500/10",
                        icon: Droplets,
                        chartData: [stats.humidity, stats.humidity, stats.humidity]
                    },
                    agriculture: {
                        val: apiData.recent_crops && apiData.recent_crops.length > 0 ? apiData.recent_crops[0].yield_amount : 0,
                        unit: "tons/ha",
                        label: "Crop Yield",
                        trend: "Stable",
                        color: "text-amber-400",
                        bg: "bg-amber-500/10",
                        icon: Sprout,
                        chartData: [4, 4.2, 4.5, 4.3, 4.5]
                    },
                    health: {
                        score: 100 - Math.round(stats.health_risk),
                        status: stats.risk_level || "Unknown",
                        desc: `Risk Factor: ${stats.risk_level || "Unknown"}. Calculated from AQI (${stats.aqi}) & Traffic.`
                    },
                    insight: `Current environment analysis: Air quality is ${(aqiStatus || "unknown").toLowerCase()} with ${(trafficStatus || "unknown").toLowerCase()} traffic flow. Health risk is ${(stats.risk_level || "unknown").toLowerCase()}. Recommended to monitor PM2.5 levels closely.`,
                    correlations: [
                        { t1: "Weather", t2: "Air Quality", desc: "Current atmospheric conditions, including wind speed and temperature, are directly influencing the dispersion of local pollutants." },
                        { t1: "Traffic", t2: "Health", desc: "Vehicular emissions from current traffic density are a significant weighted factor in the calculated public health risk index." }
                    ]
                };

                setData(transformed);
            } catch (err) {
                console.error("Dashboard fetch error", err);
                setError("Failed to load dashboard data.");
            } finally {
                setLoading(false);
            }
        };

        if (cityId) fetchData();
        window.scrollTo(0, 0);
    }, [cityId]);

    if (loading) return <div className="min-h-screen bg-slate-950 flex items-center justify-center text-cyan-400">Loading City Data...</div>;
    if (error) return <div className="min-h-screen bg-slate-950 flex items-center justify-center text-rose-400">{error}</div>;
    if (!data) return null;
    return (
        <div className="relative min-h-screen bg-slate-950 font-sans text-white selection:bg-cyan-500/30 selection:text-cyan-200">
            <ParticleBackground />
            <Navbar />

            <div className="relative z-10 pt-32 pb-20 px-6 max-w-7xl mx-auto">

                {/* Header */}
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
                    <div>
                        <Link to="/cities" className="flex items-center gap-2 text-slate-500 hover:text-cyan-400 transition-colors text-sm mb-2 group">
                            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
                            Back to Cities
                        </Link>
                        <h1 className="text-4xl md:text-5xl font-bold text-white">{data.city}</h1>
                    </div>

                    <div className="flex items-center gap-2 px-4 py-2 bg-slate-900/80 border border-slate-800 rounded-lg text-sm text-slate-400 backdrop-blur-md">
                        <Clock className="w-4 h-4" />
                        <span>Last Updated: <span className="text-white font-medium">{data.lastUpdated}</span></span>
                    </div>

                    <button
                        onClick={handleSync}
                        disabled={isSyncing}
                        className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-cyan-500/20"
                    >
                        <RefreshCw className={`w-4 h-4 ${isSyncing ? 'animate-spin' : ''}`} />
                        <span>{isSyncing ? 'Syncing Live Data...' : 'Sync Live Data'}</span>
                    </button>
                </div>

                {/* Stats Row */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">
                    {/* Left 4 Cards */}
                    <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <StatCard data={data.temp} />
                        <StatCard data={data.aqi} />
                        <StatCard data={data.traffic} />
                        <StatCard data={data.humidity} />
                    </div>

                    {/* Right Health Gauge */}
                    <div className="bg-slate-900/40 border border-slate-800 p-8 rounded-2xl backdrop-blur-sm flex flex-col items-center justify-center text-center">
                        <Gauge score={data.health.score} />
                        <div className="mt-8">
                            <h4 className="text-lg font-bold text-white mb-2">Health Index</h4>
                            <p className="text-sm text-slate-400 max-w-[200px] leading-relaxed">
                                {data.health.desc}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Insight Banner */}
                <div className="mb-12 relative overflow-hidden rounded-xl bg-slate-900/60 border-l-4 border-cyan-500 p-8 backdrop-blur-md shadow-2xl">
                    <div className="relative z-10 flex items-start gap-4">
                        <div className="w-10 h-10 rounded-lg bg-cyan-500/10 flex items-center justify-center shrink-0">
                            <TrendingUp className="w-5 h-5 text-cyan-400" />
                        </div>
                        <div>
                            <h3 className="text-lg font-bold text-white mb-2">Live System Environment Insight</h3>
                            <p className="text-slate-300 leading-relaxed">{data.insight}</p>
                        </div>
                    </div>
                </div>

                {/* Domain Overview */}
                <div className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-6">Domain Overview</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                        <DomainCard title="Weather" value={data.temp.val} unit={data.temp.unit} color={data.temp.color} icon={Thermometer} chartData={data.temp.chartData} status={data.temp.trend} />
                        <DomainCard title="Air Quality" value={data.aqi.val} unit="AQI" color={data.aqi.color} icon={Wind} chartData={data.aqi.chartData} status={data.aqi.trend} />
                        <DomainCard title="Traffic" value={data.traffic.val} unit="/10" color={data.traffic.color} icon={Car} chartData={data.traffic.chartData} status={data.traffic.trend} />
                        <DomainCard title="Agriculture" value={data.agriculture.val} unit={data.agriculture.unit} color={data.agriculture.color} icon={Sprout} chartData={data.agriculture.chartData} status="Harvesting" />
                        <DomainCard title="Health Index" value={data.health.score} unit="/100" color="text-rose-400" icon={Activity} chartData={data.health.chartData || [80, 82, 85, 83, 84, 83, 83]} status={data.health.status} />
                    </div>
                </div>

                {/* System Correlations */}
                <div>
                    <h2 className="text-2xl font-bold text-white mb-6">System Correlations</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {data.correlations.map((corr, i) => (
                            <div key={i} className="bg-slate-900/40 border-l-4 border-blue-500 p-6 rounded-r-xl backdrop-blur-sm flex items-start gap-4 hover:bg-slate-900/60 transition-colors">
                                <div className="mt-1">
                                    <Info className="w-5 h-5 text-blue-500" />
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold text-white mb-2">{corr.t1} <span className="text-slate-500">→</span> {corr.t2}</h3>
                                    <p className="text-slate-400 text-sm leading-relaxed">
                                        {corr.desc}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </div>
        </div>
    );
};

export default DashboardPage;
