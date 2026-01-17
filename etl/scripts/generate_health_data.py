import pandas as pd

# -------------------------
# Load dependent datasets
# -------------------------
weather = pd.read_csv("weather.csv")
aqi = pd.read_csv("aqi.csv")

# Ensure date format consistency
weather["date"] = pd.to_datetime(weather["date"])
aqi["date"] = pd.to_datetime(aqi["date"])

# -------------------------
# Merge on city + date
# -------------------------
df = pd.merge(
    weather,
    aqi,
    on=["city", "date"],
    how="inner"
)

# -------------------------
# Health score computation
# -------------------------
def compute_health_score(row):
    aqi_norm = (row["aqi"] / 500) * 100
    heat_stress = max(0, (row["temperature"] - 30) * 2)
    humidity_stress = (row["humidity"] / 100) * 100

    score = (
        0.6 * aqi_norm +
        0.25 * heat_stress +
        0.15 * humidity_stress
    )

    return round(min(100, score), 2)

df["health_risk_score"] = df.apply(compute_health_score, axis=1)

# -------------------------
# Risk classification
# -------------------------
def classify(score):
    if score < 35:
        return "Low"
    elif score < 65:
        return "Medium"
    else:
        return "High"

df["risk_level"] = df["health_risk_score"].apply(classify)

# -------------------------
# Select final columns
# -------------------------
health_df = df[["city", "date", "health_risk_score", "risk_level"]]

# -------------------------
# Save CSV
# -------------------------
health_df.to_csv("health.csv", index=False)

print("✅ Derived historical health.csv generated successfully.")
