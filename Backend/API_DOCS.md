# 📘 UrbanNexus API Documentation

**Base URL**: `http://localhost:8000/api/`

---

## ⚡ Quick Summary (Endpoints)

| Resource | Method | URL | Description |
| :--- | :--- | :--- | :--- |
| **Dashboard** | `GET` | `/dashboard/?city_id=1` | **Aggregation API** for Frontend. Returns Latest Stats. |
| **Cities** | `GET`/`POST` | `/cities/` | Manage supported cities. |
| **Weather** | `GET`/`POST` | `/weather/` | Daily weather logs. |
| **Air Quality** | `GET`/`POST` | `/air-quality/` | Daily AQI/Pollution logs. |
| **Traffic** | `GET`/`POST` | `/traffic/` | Daily congestion logs. |
| **Agriculture** | `GET`/`POST` | `/agriculture/` | Crop yields and soil logs. |
| **Health** | `GET`/`POST` | `/health/` | Derived health risk scores. |

---

## 🚀 1. Dashboard API (For Ishan)
This is the **Main API** for the City Dashboard page.

**Request:**
`GET /api/dashboard/?city_id=1`

**Response:**
```json
{
    "city": "Delhi",
    "state": "Delhi",
    "latest_stats": {
        "temperature": 29.5,
        "humidity": 45.0,
        "aqi": 350,
        "pm25": 210.5,
        "traffic_density": 9,
        "health_risk": 85.0,
        "risk_level": "High"
    },
    "recent_crops": [
        {
            "id": 1,
            "city_name": "Delhi",
            "date": "2023-11-01",
            "crop_type": "Wheat",
            "yield_amount": 4.5,
            "soil_moisture": 30.2,
            "city": 2
        }
    ]
}
```

---

## 🏙️ 2. Cities
**Create City:**
`POST /api/cities/`
```json
{
    "city_name": "Mumbai",
    "state": "Maharashtra",
    "latitude": 19.0760,
    "longitude": 72.8777
}
```

---

## 🌤️ 3. Weather
**Add Weather Log:**
`POST /api/weather/`
```json
{
    "city": 1,
    "date": "2023-10-27",
    "temperature": 32.5,
    "humidity": 78.0,
    "rainfall": 12.4
}
```

---

## 🌫️ 4. Air Quality
**Add Pollution Log:**
`POST /api/air-quality/`
```json
{
    "city": 1,
    "date": "2023-10-27",
    "aqi": 150,
    "pm25": 60.5,
    "pm10": 110.2,
    "no2": 40.0
}
```

---

## 🌾 5. Agriculture
**Add Crop Data:**
`POST /api/agriculture/`
```json
{
    "city": 1,
    "date": "2023-11-01",
    "crop_type": "Wheat",
    "yield_amount": 4.5,
    "soil_moisture": 30.2
}
```

---

## ❤️ 6. Health Index (For Kavish/Analytics)
**Add Risk Score:**
`POST /api/health/`
```json
{
    "city": 1,
    "date": "2023-11-01",
    "health_risk_score": 88.5,
    "risk_level": "High"
}
```
