from analytics.services.health_risk import compute_health_risk


def simulate_scenario(weather, air, agri, traffic, scenario):

    # 1. Traffic Logic
    air.aqi *= (1 - scenario.get("traffic_reduction", 0))
    traffic.traffic_density *= (1 - scenario.get("traffic_reduction", 0))

    # 2. Agriculture Logic (Investment + Weather Impact)
    # Base boost from policy
    yield_multiplier = (1 + scenario.get("agri_boost", 0))

    # Add Weather Impact (The Missing Link)
    current_rain = weather.rainfall
    if current_rain < 2: 
        yield_multiplier *= 0.8 # Drought penalty (-20%)
    elif current_rain > 50: 
        yield_multiplier *= 0.6 # Flood penalty (-40%)
    
    agri.yield_amount *= yield_multiplier

    score, level = compute_health_risk(weather, air, agri, traffic)

    return score, level
