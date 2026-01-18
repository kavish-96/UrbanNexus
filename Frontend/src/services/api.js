import axios from 'axios';

const api = axios.create({
    baseURL: 'http://120.120.122.174:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getCities = async () => {
    try {
        const response = await api.get('/cities/');
        return response.data;
    } catch (error) {
        console.error("Error fetching cities:", error);
        throw error;
    }
};

export const getDashboardData = async (cityId) => {
    try {
        const response = await api.get(`/dashboard/?city_id=${cityId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching dashboard data:", error);
        throw error;
    }
};

export const getWeather = async () => {
    try {
        const response = await api.get('/weather/');
        return response.data;
    } catch (error) {
        console.error("Error fetching weather:", error);
        throw error;
    }
};

export const getAirQuality = async () => {
    try {
        const response = await api.get('/air-quality/');
        return response.data;
    } catch (error) {
        console.error("Error fetching air quality:", error);
        throw error;
    }
};

export const getTraffic = async () => {
    try {
        const response = await api.get('/traffic/');
        return response.data;
    } catch (error) {
        console.error("Error fetching traffic:", error);
        throw error;
    }
};

export const getAgriculture = async () => {
    try {
        const response = await api.get('/agriculture/');
        return response.data;
    } catch (error) {
        console.error("Error fetching agriculture:", error);
        throw error;
    }
};

export const getHealth = async () => {
    try {
        const response = await api.get('/health/');
        return response.data;
    } catch (error) {
        console.error("Error fetching health data:", error);
        throw error;
    }
};

// --- POST Methods (Data Submission) ---

export const createCity = async (cityData) => {
    try {
        const response = await api.post('/cities/', cityData);
        return response.data;
    } catch (error) {
        console.error("Error creating city:", error);
        throw error;
    }
};

export const createWeatherLog = async (weatherData) => {
    try {
        const response = await api.post('/weather/', weatherData);
        return response.data;
    } catch (error) {
        console.error("Error creating weather log:", error);
        throw error;
    }
};

export const createAirQualityLog = async (aqiData) => {
    try {
        const response = await api.post('/air-quality/', aqiData);
        return response.data;
    } catch (error) {
        console.error("Error creating air quality log:", error);
        throw error;
    }
};

export const createTrafficLog = async (trafficData) => {
    try {
        const response = await api.post('/traffic/', trafficData);
        return response.data;
    } catch (error) {
        console.error("Error creating traffic log:", error);
        throw error;
    }
};

export const createAgricultureLog = async (agriData) => {
    try {
        const response = await api.post('/agriculture/', agriData);
        return response.data;
    } catch (error) {
        console.error("Error creating agriculture log:", error);
        throw error;
    }
};

export const createHealthLog = async (healthData) => {
    try {
        const response = await api.post('/health/', healthData);
        return response.data;
    } catch (error) {
        console.error("Error creating health log:", error);
        throw error;
    }
};

export const runSimulation = async (cityId, scenarioData) => {
    // scenarioData format: { temperature: 30, traffic: 8, rain: 0 }
    // endpoint: /analytics/simulate/<city_id>/
    try {
        const response = await api.post(`/analytics/simulate/${cityId}/`, scenarioData);
        return response.data;
    } catch (error) {
        console.error("Simulation failed:", error);
        throw error;
    }
};

export default api;
