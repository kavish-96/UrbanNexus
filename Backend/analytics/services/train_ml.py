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

# 3. Calculate Target (Health Risk Score)
# Logic: Risk = (AQI * 0.4) + (Traffic * 0.3) + (|Temp - 25| * 1.0)
print("Calculating Health Risk Labels...")
df['temp_stress'] = abs(df['temperature'] - 25)
df['health_risk_score'] = (
    (df['aqi'] * 0.4) + 
    (df['traffic_density'] * 5.0) + 
    (df['temp_stress'] * 2.0)
)
# Normalize to 0-100
df['health_risk_score'] = df['health_risk_score'].clip(0, 100)

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
