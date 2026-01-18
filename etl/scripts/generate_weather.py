import pandas as pd
import random
from datetime import date, timedelta

# -------------------------
# Config
# -------------------------
CITY = "Delhi"
START_DATE = date(2017, 1, 1)
END_DATE = date(2024, 1, 1)

# -------------------------
# Helper functions
# -------------------------
def temperature_range(month):
    if month in (12, 1):
        return 5, 20
    elif month in (2, 3):
        return 12, 30
    elif month in (4, 5, 6):
        return 25, 45
    elif month in (7, 8, 9):
        return 25, 35
    else:
        return 15, 30


def humidity_range(month):
    if month in (7, 8, 9):
        return 60, 95
    elif month in (4, 5, 6):
        return 20, 60
    else:
        return 40, 90


def rainfall_amount(month):
    if month in (7, 8, 9):
        return round(random.choice([0, 0, 0, random.uniform(1, 50)]), 1)
    else:
        return round(random.choice([0, 0, random.uniform(0, 5)]), 1)

# -------------------------
# Generate data
# -------------------------
rows = []
current = START_DATE

while current <= END_DATE:
    t_min, t_max = temperature_range(current.month)
    h_min, h_max = humidity_range(current.month)

    temperature = round(random.uniform(t_min, t_max), 1)
    humidity = random.randint(h_min, h_max)
    rainfall = rainfall_amount(current.month)

    # HARD SAFETY CLAMPS (non-negotiable)
    temperature = max(-5, min(50, temperature))
    humidity = max(0, min(100, humidity))
    rainfall = max(0, rainfall)

    rows.append({
        "city": CITY,
        "date": current.isoformat(),
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall
    })

    current += timedelta(days=1)

# -------------------------
# Save CSV
# -------------------------
df = pd.DataFrame(rows)
df.to_csv("weather.csv", index=False)

print("✅ Realistic weather.csv generated successfully.")
