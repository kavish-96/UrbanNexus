import pandas as pd
import random
from datetime import date, timedelta

# -------------------------
# Config
# -------------------------
CITY = "Delhi"
START_DATE = date(2017, 1, 1)
END_DATE = date(2023, 7, 11)

# -------------------------
# Helper functions
# -------------------------
def aqi_range(month):
    if month in (11, 12, 1):
        return 300, 500        # Winter
    elif month in (2, 3):
        return 200, 350        # Pre-summer
    elif month in (4, 5, 6):
        return 150, 300        # Summer
    elif month in (7, 8, 9):
        return 50, 150         # Monsoon
    else:
        return 200, 350        # October

def pollutants_from_aqi(aqi):
    # Rough but realistic relationships
    pm25 = round(aqi * random.uniform(0.65, 0.8))
    pm10 = round(pm25 * random.uniform(1.2, 1.4))
    no2  = round(random.uniform(15, 100))

    return pm25, pm10, no2

# -------------------------
# Generate data
# -------------------------
rows = []
current = START_DATE

while current <= END_DATE:
    aqi_min, aqi_max = aqi_range(current.month)
    aqi = random.randint(aqi_min, aqi_max)

    pm25, pm10, no2 = pollutants_from_aqi(aqi)

    # HARD SAFETY RULES
    aqi = max(0, min(500, aqi))
    pm25 = max(0, pm25)
    pm10 = max(pm25, pm10)   # enforce pm10 ≥ pm25
    no2 = max(10, no2)       # urban minimum

    rows.append({
        "city": CITY,
        "date": current.isoformat(),
        "aqi": aqi,
        "pm25": pm25,
        "pm10": pm10,
        "no2": no2
    })

    current += timedelta(days=1)

# -------------------------
# Save CSV
# -------------------------
df = pd.DataFrame(rows)
df.to_csv("aqi.csv", index=False)

print("✅ Realistic aqi.csv generated successfully.")
