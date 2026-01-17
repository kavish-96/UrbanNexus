from analytics.services.health_risk import compute_health_risk


def simulate_scenario(weather, air, agri, traffic, scenario):

    air.aqi *= (1 - scenario.get("traffic_reduction", 0))
    traffic.traffic_density *= (1 - scenario.get("traffic_reduction", 0))

    agri.yeild *= (1 + scenario.get("agri_boost", 0))

    score, level = compute_health_risk(weather, air, agri, traffic)

    return score, level
