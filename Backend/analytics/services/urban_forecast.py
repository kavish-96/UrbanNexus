import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

MODEL_PATH = "analytics/models/urban_forecast.pkl"


def train_model(queryset):

    data = []

    for row in queryset:
        data.append(
            {
                "aqi": row.air_quality.aqi,
                "temperature": row.weather.temperature,
                "humidity": row.weather.humidity,
                "rainfall": row.weather.rainfall,
                "traffic_density": row.traffic.traffic_density,
                "yield": row.agriculture.yeild,
                "health_risk_score": row.health_index.health_risk_score
            }
        )

    df = pd.DataFrame(data)

    X = df[[
        "aqi", "temperature", "humidity",
        "rainfall", "traffic_density", "yield"
    ]]
    y = df["health_risk_score"]

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    return model


def load_model():
    return joblib.load(MODEL_PATH)


def predict_risk(model, features):

    df = pd.DataFrame([features])
    prediction = model.predict(df)[0]

    return round(float(prediction), 2)
