import pandas as pd
import random
from datetime import date, timedelta

# -------------------------
# Config
# -------------------------
CITY = "Delhi"
START_DATE = date(2023, 1, 1)
END_DATE = date(2024, 1, 1)

# -------------------------
# Helper functions
# -------------------------
def density_by_day(day_of_week):
    # 0 = Monday, 6 = Sunday
    if day_of_week < 5:       # Weekday
        return random.randint(6, 9)
    else:                     # Weekend
        return random.randint(2, 6)

def speed_from_density(density):
    if density <= 2:
        return random.randint(45, 60)
    elif density <= 4:
        return random.randint(35, 50)
    elif density <= 6:
        return random.randint(25, 40)
    elif density <= 8:
        return random.randint(15, 25)
    else:
        return random.randint(5, 15)

# -------------------------
# Generate data
# -------------------------
rows = []
current = START_DATE

while current <= END_DATE:
    density = density_by_day(current.weekday())
    speed = speed_from_density(density)

    # HARD SAFETY CLAMPS
    density = max(1, min(10, density))
    speed = max(5, min(60, speed))

    rows.append({
        "city": CITY,
        "date": current.isoformat(),
        "traffic_density": density,
        "avg_speed": speed
    })

    current += timedelta(days=1)

# -------------------------
# Save CSV
# -------------------------
df = pd.DataFrame(rows)
df.to_csv("traffic.csv", index=False)

print("✅ Realistic traffic.csv generated successfully.")