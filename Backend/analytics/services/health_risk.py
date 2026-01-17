import numpy as np

# Normalization helpers
def normalize(value, min_val, max_val):
    if value is None:
        return 0
    return max(0, min(1, (value - min_val) / (max_val - min_val)))


def compute_health_risk(weather, air, agri, traffic):

    norm_aqi = normalize(air.aqi, 0, 500)
    norm_temp = normalize(weather.temperature, 0, 50)
    norm_humidity = normalize(weather.humidity, 0, 100)

    # proxies
    traffic_stress = normalize(traffic.traffic_density, 1, 10)
    food_stress = normalize(agri.yeild, 0, 10)

    risk = (
        0.30 * norm_aqi +
        0.20 * norm_temp +
        0.15 * norm_humidity +
        0.20 * traffic_stress +
        0.15 * food_stress
    )

    score = round(risk * 100, 2)

    if score < 35:
        level = "Low"
    elif score < 65:
        level = "Medium"
    else:
        level = "High"

    return score, level

