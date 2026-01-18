import numpy as np

# Normalization helpers
def normalize(value, min_val, max_val):
    if value is None:
        return 0
    return max(0, min(1, (value - min_val) / (max_val - min_val)))


def compute_health_risk(weather, air, agri, traffic):
    """
    Computes a sophisticated Urban Health Risk Score (0-100).
    Logic based on WHO Guidelines & Urban Planning Standards.
    """

    # --- 1. Air Quality (Exponential Decay) ---
    # AQI > 300 is hazardous. We punish high values more severely.
    # Formula: Risk increases sharply after AQI 150.
    aqi_risk = 0
    if air.aqi <= 50: aqi_risk = 0
    elif air.aqi <= 100: aqi_risk = 0.2
    elif air.aqi <= 200: aqi_risk = 0.5
    elif air.aqi <= 300: aqi_risk = 0.8
    else: aqi_risk = 1.0

    # --- 2. Temperature (Comfort Zone) ---
    # Ideal: 20C - 30C. Risk only starts outside this buffer.
    temp = weather.temperature
    temp_risk = 0
    if temp < 10: temp_risk = (10 - temp) / 10 # Cold Stress
    elif temp > 35: temp_risk = (temp - 35) / 15 # Heat Stress
    # Buffer 10-35 is treated as "Low/Manageable Risk" (0 to 0.1 linear) to keep score dynamic
    else: temp_risk = 0.1 
    temp_risk = min(1.0, temp_risk)

    # --- 3. Rainfall (Flood vs Drought) ---
    # > 50mm is flood risk.
    rain = weather.rainfall
    rain_risk = 0
    if rain > 50: rain_risk = (rain - 50) / 100
    rain_risk = min(1.0, rain_risk)

    # --- 4. Traffic (Congestion Stress) ---
    # Density 1-10. 
    # >7 is severe congestion.
    traffic_val = traffic.traffic_density
    traffic_risk = traffic_val / 10.0

    # --- 5. Food Security (Logarithmic Safety) ---
    # Yield > 3 tons/ha is 'Safe'. < 1 is 'Starvation'.
    # We invert it: Low Yield = High Risk.
    yield_val = getattr(agri, 'yield_amount', 0)
    food_risk = 1.0
    if yield_val >= 4: food_risk = 0.0
    elif yield_val >= 2: food_risk = 0.2
    else: food_risk = 1.0 - (yield_val / 2.0) # Linearly increase risk as yield drops below 2
    food_risk = max(0.0, food_risk)


    # --- WEIGHTED SUM ---
    # AQI is the #1 silent killer in cities (35%)
    # Food is survival (20%)
    # Traffic is mental stress (15%)
    # Temp/Rain are environmental (30%)
    
    total_risk = (
        0.35 * aqi_risk +
        0.20 * food_risk +
        0.15 * traffic_risk +
        0.20 * temp_risk +
        0.10 * rain_risk
    )

    score = round(total_risk * 100, 2)
    
    # Cap at 100
    score = min(100, score)

    if score < 30: level = "Low"
    elif score < 70: level = "Medium"
    else: level = "High"

    return score, level

