import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

# Define Paths
# UrbanNexus/Backend/analytics/services/train_ml.py
# We need to go up 4 levels: services -> analytics -> Backend -> UrbanNexus
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CSV_DIR = os.path.join(BASE_DIR, "etl", "data_sources", "csv")
MODEL_DIR = os.path.join(BASE_DIR, "Backend", "analytics", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "urban_forecast.pkl")

print(f"Loading data from {CSV_DIR}...")

# 1. Load Data
try:
    weather = pd.read_csv(os.path.join(CSV_DIR, "weather.csv"))
    air = pd.read_csv(os.path.join(CSV_DIR, "aqi.csv"))
    traffic = pd.read_csv(os.path.join(CSV_DIR, "traffic.csv"))
    agri = pd.read_csv(os.path.join(CSV_DIR, "agriculture.csv"))
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

# 1b. Map City Names to IDs (since CSVs have names, but we merge on ID or Name)
city_map = {
    'Mumbai': 1,
    'Delhi': 2,
    'Bangalore': 3,
    'Chennai': 4,
    'Kolkata': 5
}

def add_city_id(df):
    if 'city' in df.columns:
        df['city_id'] = df['city'].map(city_map)
        df = df.drop(columns=['city']) # Prevent merge conflicts
    return df

weather = add_city_id(weather)
air = add_city_id(air)
traffic = add_city_id(traffic)
agri = add_city_id(agri)

# Drop rows where city_id is NaN (if any unknown cities)
weather = weather.dropna(subset=['city_id'])
air = air.dropna(subset=['city_id'])
traffic = traffic.dropna(subset=['city_id'])
agri = agri.dropna(subset=['city_id'])

# Ensure dates are strings for merging
weather['date'] = weather['date'].astype(str)
air['date'] = air['date'].astype(str)
traffic['date'] = traffic['date'].astype(str)
agri['date'] = agri['date'].astype(str)

print("Merging datasets...")
# Merge Weather + Air
df = pd.merge(weather, air, on=['city_id', 'date'], how='inner')

# Merge + Traffic (Traffic data is smaller, so use inner to keep valid training set)
df = pd.merge(df, traffic, on=['city_id', 'date'], how='inner')
# Merge + Agri (Optional, use left if agri is sparse, but inner for strong training)
df = pd.merge(df, agri, on=['city_id', 'date'], how='left')

# Fill missing agri values with mean
if 'yield' in df.columns:
    df['yield'] = df['yield'].fillna(df['yield'].mean())
else:
    # If different column name
    df['yield'] = 4.0 # Default fallback

# 3. Calculate Target (Health Risk Score) - SCIENTIFIC FORMULA
# Logic: Risk = 0.35(AQI) + 0.20(Traffic) + 0.15(TempDev) + 0.15(Hum) + 0.15(FoodSec)

# 3. Calculate Target (Health Risk Score) - PROFESSIONAL LOGIC

def calculate_row_risk(row):
    # AQI
    aqi = row['aqi']
    if aqi <= 50: aqi_risk = 0
    elif aqi <= 100: aqi_risk = 0.2
    elif aqi <= 200: aqi_risk = 0.5
    elif aqi <= 300: aqi_risk = 0.8
    else: aqi_risk = 1.0

    # Temp
    temp = row['temperature']
    if temp < 10: temp_risk = (10 - temp) / 10
    elif temp > 35: temp_risk = (temp - 35) / 15
    else: temp_risk = 0.1
    temp_risk = min(1.0, max(0.0, temp_risk))

    # Rain
    rain = row.get('rainfall', 0)
    if rain > 50: rain_risk = (rain - 50) / 100
    else: rain_risk = 0
    rain_risk = min(1.0, rain_risk)

    # Traffic
    traffic_risk = row['traffic_density'] / 10.0

    # Food
    yield_val = row.get('yield', 0)
    if yield_val >= 4: food_risk = 0.0
    elif yield_val >= 2: food_risk = 0.2
    else: food_risk = 1.0 - (yield_val / 2.0)
    food_risk = max(0.0, food_risk)

    total = (
        0.35 * aqi_risk +
        0.20 * food_risk +
        0.15 * traffic_risk +
        0.20 * temp_risk +
        0.10 * rain_risk
    )
    return round(min(100, total * 100), 2)

print("Calculating Health Risk Labels (Professional Model)...")
df['health_risk_score'] = df.apply(calculate_row_risk, axis=1)

# Handle duplicate rainfall columns (rainfall_x from weather, rainfall_y from agri)
if 'rainfall_x' in df.columns:
    df.rename(columns={'rainfall_x': 'rainfall'}, inplace=True)

# 4. Train Model
print("Available columns:", df.columns.tolist()) # Debug line
X = df[['aqi', 'temperature', 'humidity', 'rainfall', 'traffic_density', 'yield']]
y = df['health_risk_score']

print(f"Training RandomForest on {len(df)} records...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 5. Save Model
print(f"Saving model to {MODEL_PATH}...")
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
joblib.dump(model, MODEL_PATH)

print("✅ Model Trained and Saved Successfully!")
