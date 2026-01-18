import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FlaskConical, RotateCcw, Thermometer, Car, CloudRain, Zap } from 'lucide-react';
import Navbar from '../components/Navbar';
import ParticleBackground from '../components/ParticleBackground';
import { getDashboardData } from '../services/api';

const SimulationPage = () => {
    const { cityId } = useParams();

    // --- State ---
    const [temp, setTemp] = useState(20);
    const [traffic, setTraffic] = useState(2);
    const [rain, setRain] = useState(0);

    // UI Results
    const [resultScore, setResultScore] = useState(0);
    const [aqiChange, setAqiChange] = useState(0);
    const [cropImpact, setCropImpact] = useState(0);
    const [scoreDelta, setScoreDelta] = useState(0);
    const [baseScore, setBaseScore] = useState(72);

    // --- Load Live Data (Sync with Dashboard) ---
    useEffect(() => {
        const fetchBaseline = async () => {
            if (!cityId) return;
            try {
                const data = await getDashboardData(cityId);
                const stats = data.latest_stats;

                if (stats) {
                    setTemp(stats.temperature || 20);
                    setTraffic(stats.traffic_density || 2);
                    setRain(stats.rainfall || 0); // Rainfall isn't always in stats snippet, but let's assume valid
                    setBaseScore(100 - (stats.health_risk || 20)); // Approximate base
                }
            } catch (err) {
                console.error("Failed to load baseline sim data", err);
            }
        };
        fetchBaseline();
    }, [cityId]);

    // --- Logic ---
    useEffect(() => {
        // Simple impact logic for demo
        // Ideal: Temp 22, Traffic 2, Rain 30

        // Temp penalty: -1.5 points per degree away from 22
        const tempPenalty = Math.abs(temp - 22) * 1.5;

        // Traffic penalty: -3 points per level
        const trafficPenalty = traffic * 3;

        // Rain bonus/penalty: 
        // 10-40mm is ideal (clean air). Too little = dust. Too much = flood risk/overcast.
        let rainEffect = 0;
        if (rain >= 10 && rain <= 40) rainEffect = 5; // Bonus
        else if (rain === 0) rainEffect = -5; // Dust
        else if (rain > 80) rainEffect = -10; // Storm

        let calculated = 100 - tempPenalty - trafficPenalty + rainEffect;
        calculated = Math.min(100, Math.max(0, Math.round(calculated)));

        setResultScore(calculated);
        setScoreDelta(calculated - baseScore);

        // AQI Change: Driven by Traffic and Heat
        // Baseline traffic 3. Each level > 3 adds 15 AQI. Heat > 25 adds 2 AQI/deg. Rain reduces AQI.
        let aqiDelta = (traffic - 3) * 10 + Math.max(0, temp - 25) * 2 - (rain > 5 ? 20 : 0);
        setAqiChange(Math.round(aqiDelta));

        // Crop Yield: Driven by Rain and Temp
        // Ideal: Temp 20-30, Rain 20-60.
        let crop = 0;
        if (temp > 35) crop -= 20;
        if (temp < 10) crop -= 30;
        if (rain < 5) crop -= 15;
        if (rain > 80) crop -= 10;
        setCropImpact(crop);

    }, [temp, traffic, rain, baseScore]);

    const handleReset = () => {
        setTemp(22);
        setTraffic(2);
        setRain(30);
    };

    // --- Components ---
    const Slider = ({ label, icon: Icon, value, min, max, unit, onChange, color, labels }) => {
        const percent = ((value - min) / (max - min)) * 100;
        const colorName = color.split('-')[1]; // e.g. 'cyan', 'purple', 'blue'

        // Map for gradient background (Hex values for Tailwind 400 shades)
        const colorMap = {
            cyan: '#22d3ee',
            purple: '#c084fc',
            blue: '#60a5fa',
        };
        const activeColor = colorMap[colorName] || '#22d3ee';

        return (
            <div className="mb-8">
                <div className="flex justify-between items-center mb-4">
                    <div className="flex items-center gap-2 text-slate-300 font-medium">
                        <Icon className={`w-5 h-5 ${color}`} />
                        {label}
                    </div>
                    <div className={`text-xl font-bold ${color}`}>
                        {value}{unit}
                    </div>
                </div>
                <input
                    type="range"
                    min={min}
                    max={max}
                    value={value}
                    onChange={(e) => onChange(Number(e.target.value))}
                    style={{
                        background: `linear-gradient(to right, ${activeColor} 0%, ${activeColor} ${percent}%, #1e293b ${percent}%, #1e293b 100%)`
                    }}
                    className={`
                        w-full h-2 rounded-lg appearance-none cursor-pointer outline-none
                        [&::-webkit-slider-thumb]:appearance-none
                        [&::-webkit-slider-thumb]:w-6 [&::-webkit-slider-thumb]:h-6
                        [&::-webkit-slider-thumb]:rounded-full
                        [&::-webkit-slider-thumb]:bg-slate-950
                        [&::-webkit-slider-thumb]:border-2
                        [&::-webkit-slider-thumb]:border-${colorName}-400
                        [&::-webkit-slider-thumb]:transition-transform
                        [&::-webkit-slider-thumb]:hover:scale-110
                        
                        [&::-moz-range-thumb]:w-6 [&::-moz-range-thumb]:h-6
                        [&::-moz-range-thumb]:rounded-full
                        [&::-moz-range-thumb]:bg-slate-950
                        [&::-moz-range-thumb]:border-2
                        [&::-moz-range-thumb]:border-${colorName}-400
                        [&::-moz-range-thumb]:transition-transform
                        [&::-moz-range-thumb]:hover:scale-110
                    `}
                />
                <div className="flex justify-between text-xs text-slate-500 mt-2 font-mono">
                    <span>{labels[0]}</span>
                    <span>{labels[1]}</span>
                </div>
            </div>
        );
    };

    const Gauge = ({ score, title, color }) => {
        const radius = 56;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (score / 100) * circumference;

        return (
            <div className="flex flex-col items-center justify-center p-8 bg-slate-900/40 border border-slate-800 rounded-2xl backdrop-blur-sm">
                <h3 className={`text-sm font-medium mb-6 ${color === 'text-cyan-400' ? 'text-slate-400' : 'text-cyan-400'}`}>{title}</h3>
                <div className="relative w-40 h-40 flex items-center justify-center">
                    {/* Track */}
                    <svg className="w-full h-full transform -rotate-90">
                        <circle
                            cx="80"
                            cy="80"
                            r={radius}
                            stroke="#1e293b"
                            strokeWidth="12"
                            fill="transparent"
                        />
                        <circle
                            cx="80"
                            cy="80"
                            r={radius}
                            stroke="currentColor"
                            strokeWidth="12"
                            fill="transparent"
                            strokeDasharray={circumference}
                            strokeDashoffset={offset}
                            strokeLinecap="round"
                            className={`transition-all duration-500 ease-out ${score > 70 ? 'text-emerald-500' : score > 40 ? 'text-amber-500' : 'text-rose-500'}`}
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className={`text-5xl font-bold ${score > 70 ? 'text-emerald-400' : score > 40 ? 'text-amber-400' : 'text-rose-400'}`}>
                            {score}
                        </span>
                        <span className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold mt-1">Health Score</span>
                    </div>
                </div>

                <div className={`mt-6 px-4 py-1.5 rounded-full text-xs font-bold text-slate-950 ${score > 70 ? 'bg-emerald-400' : score > 40 ? 'bg-amber-400' : 'bg-rose-400'}`}>
                    {score > 70 ? 'Low Risk' : score > 40 ? 'Moderate' : 'Critical'}
                </div>
            </div>
        );
    };

    return (
        <div className="relative min-h-screen bg-slate-950 font-sans text-white selection:bg-cyan-500/30 selection:text-cyan-200">
            <ParticleBackground />
            <Navbar />

            <div className="relative z-10 pt-32 pb-20 px-6 max-w-7xl mx-auto">
                <div className="flex items-center gap-2 text-cyan-400 mb-2 font-medium">
                    <FlaskConical className="w-5 h-5" />
                    <span>What-If Lab</span>
                </div>
                <h1 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                    Scenario Simulation
                    <span className="block md:inline md:ml-4 text-2xl md:text-3xl text-slate-500 font-normal">(Delhi Base Model)</span>
                </h1>
                <p className="text-slate-400 text-lg max-w-2xl mb-12">
                    Adjust environmental parameters and observe how changes cascade through interconnected urban systems.
                </p>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Left Panel - Parameters */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.6 }}
                        className="bg-slate-900/60 border border-slate-800 rounded-2xl p-8 backdrop-blur-md"
                    >
                        <div className="flex justify-between items-center mb-8">
                            <h2 className="text-xl font-bold text-white">Parameters</h2>
                            <button
                                onClick={handleReset}
                                className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800 text-sm text-slate-300 hover:text-white hover:border-slate-600 transition-colors"
                            >
                                <RotateCcw className="w-3.5 h-3.5" />
                                Reset
                            </button>
                        </div>

                        <Slider
                            label="Temperature"
                            icon={Thermometer}
                            value={temp}
                            min={10}
                            max={45}
                            unit="°C"
                            onChange={setTemp}
                            color="text-cyan-400"
                            labels={["10°C", "45°C"]}
                        />
                        <Slider
                            label="Traffic Density"
                            icon={Car}
                            value={traffic}
                            min={0}
                            max={10}
                            unit="/10"
                            onChange={setTraffic}
                            color="text-purple-400"
                            labels={["Light", "Severe"]}
                        />
                        <Slider
                            label="Rainfall"
                            icon={CloudRain}
                            value={rain}
                            min={0}
                            max={100}
                            unit="mm"
                            onChange={setRain}
                            color="text-blue-400"
                            labels={["0mm", "100mm"]}
                        />
                    </motion.div>

                    {/* Right Panel - Results */}
                    <div className="space-y-6">
                        {/* Gauges */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className="grid grid-cols-1 sm:grid-cols-2 gap-6"
                        >
                            <Gauge score={72} title="Current Baseline" color="text-slate-400" />
                            <Gauge score={resultScore} title="Scenario Result" color="text-cyan-400" />
                        </motion.div>

                        {/* Impact List */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.3 }}
                            className="bg-slate-900/60 border border-slate-800 rounded-2xl p-8 backdrop-blur-md"
                        >
                            <h3 className="text-lg font-bold text-white mb-6">Projected Impacts</h3>

                            <div className="space-y-6">
                                <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                                    <span className="text-slate-400">Air Quality Change</span>
                                    <span className={`font-bold ${aqiChange > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                                        {aqiChange > 0 ? '+' : ''}{aqiChange} AQI
                                    </span>
                                </div>
                                <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                                    <span className="text-slate-400">Crop Yield Impact</span>
                                    <span className={`font-bold ${cropImpact < 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                                        {cropImpact > 0 ? '+' : ''}{cropImpact}%
                                    </span>
                                </div>
                                <div className="flex justify-between items-center py-2">
                                    <span className="text-slate-400">Health Score Delta</span>
                                    <span className={`font-bold ${scoreDelta < 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                                        {scoreDelta > 0 ? '+' : ''}{scoreDelta}
                                    </span>
                                </div>
                            </div>
                        </motion.div>

                        {/* Scenario Analysis Banner */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.4 }}
                            className="bg-slate-900/60 border-l-4 border-cyan-500 p-6 rounded-r-xl backdrop-blur-md flex gap-4"
                        >
                            <div className="mt-1">
                                <Zap className="w-5 h-5 text-cyan-400" />
                            </div>
                            <div>
                                <h4 className="font-bold text-white mb-1">Scenario Analysis</h4>
                                <p className="text-slate-400 text-sm leading-relaxed">
                                    {resultScore < 50
                                        ? "Critical condition projected. High traffic and adverse weather significantly degrade urban health systems."
                                        : resultScore < 70
                                            ? "Moderate impact observed. Urban systems are stressed but stable. Mitigation strategies recommended."
                                            : "Optimal conditions maintained. Current parameters support healthy urban function."
                                    }
                                </p>
                            </div>
                        </motion.div>

                    </div>
                </div>
            </div>
        </div>
    );
};

export default SimulationPage;
