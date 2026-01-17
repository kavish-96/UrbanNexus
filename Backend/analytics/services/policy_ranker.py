from analytics.services.scenario_engine import simulate_scenario

POLICIES = {
    "Reduce Traffic 20%": {"traffic_reduction": 0.2},
    "Reduce Traffic 40%": {"traffic_reduction": 0.4},
    "Boost Agriculture 20%": {"agri_boost": 0.2},
}


def rank_policies(weather, air, agri, traffic):

    results = []

    for name, scenario in POLICIES.items():
        score, _ = simulate_scenario(weather, air, agri, traffic, scenario)
        results.append({
            "policy": name,
            "projected_risk": score
        })

    return sorted(results, key=lambda x: x["projected_risk"])
