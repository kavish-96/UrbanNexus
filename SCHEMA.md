# UrbanNexus – Database Schema (Final, Optimized)

⚠️ This schema is FINAL and frozen for the hackathon.
Designed for scalability, analytics performance, and Django compatibility.

---

## 🏙️ city (Master / Dimension Table)

Stores static information about cities.

| Column    | Data Type    | Description                    |
| --------- | ------------ | ------------------------------ |
| city_id   | SERIAL (PK)  | Auto-increment city identifier |
| city_name | VARCHAR(100) | City name                      |
| state     | VARCHAR(100) | State name                     |
| latitude  | DECIMAL(9,6) | Geographic latitude            |
| longitude | DECIMAL(9,6) | Geographic longitude           |

---

## 🌦️ weather_data (Time-Series)

Daily aggregated weather data per city.

| Column      | Data Type               | Description         |
| ----------- | ----------------------- | ------------------- |
| id          | BIGSERIAL (PK)          | Unique record ID    |
| city_id     | INT (FK → city.city_id) | City reference      |
| date        | DATE                    | Observation date    |
| temperature | REAL                    | Temperature in °C   |
| humidity    | REAL                    | Humidity percentage |
| rainfall    | REAL                    | Rainfall in mm      |
| ingested_at | TIMESTAMP               | Data ingestion time |

Index recommendation:
(city_id, date)

---

## 🌫️ air_quality (Time-Series)

Daily air quality measurements per city.

| Column      | Data Type               | Description         |
| ----------- | ----------------------- | ------------------- |
| id          | BIGSERIAL (PK)          | Unique record ID    |
| city_id     | INT (FK → city.city_id) | City reference      |
| date        | DATE                    | Observation date    |
| aqi         | SMALLINT                | Air Quality Index   |
| pm25        | REAL                    | PM2.5 concentration |
| pm10        | REAL                    | PM10 concentration  |
| no2         | REAL                    | NO2 concentration   |
| ingested_at | TIMESTAMP               | Data ingestion time |

Index recommendation:
(city_id, date)

---

## 🚦 traffic_data (Time-Series)

Traffic congestion data per city.

| Column          | Data Type               | Description                  |
| --------------- | ----------------------- | ---------------------------- |
| id              | BIGSERIAL (PK)          | Unique record ID             |
| city_id         | INT (FK → city.city_id) | City reference               |
| date            | DATE                    | Observation date             |
| traffic_density | SMALLINT                | Congestion level (1–10)      |
| avg_speed       | REAL                    | Average vehicle speed (km/h) |
| ingested_at     | TIMESTAMP               | Data ingestion time          |

Index recommendation:
(city_id, date)

---

## 🌱 agriculture_data (Time-Series)

Agricultural indicators linked to city regions.

| Column        | Data Type               | Description              |
| ------------- | ----------------------- | ------------------------ |
| id            | BIGSERIAL (PK)          | Unique record ID         |
| city_id       | INT (FK → city.city_id) | City reference           |
| date          | DATE                    | Observation date         |
| crop_type     | VARCHAR(50)             | Crop name                |
| yield         | REAL                    | Yield (ton/ha)           |
| soil_moisture | REAL                    | Soil moisture percentage |

Index recommendation:
(city_id, date)

---

## ❤️ health_index (Derived / Analytics Table)

Derived health risk indicators based on environmental factors.

| Column            | Data Type               | Description         |
| ----------------- | ----------------------- | ------------------- |
| id                | BIGSERIAL (PK)          | Unique record ID    |
| city_id           | INT (FK → city.city_id) | City reference      |
| date              | DATE                    | Observation date    |
| health_risk_score | REAL                    | Risk score (0–100)  |
| risk_level        | VARCHAR(10)             | Low / Medium / High |

Index recommendation:
(city_id, date)

---

## 📈 Design Notes

- Fact tables use BIGSERIAL for long-term scalability
- DATE is used instead of TIMESTAMP for analytics simplicity
- REAL is chosen for performance in aggregations & ML
- Schema follows star-like design (dimension + facts)
- Fully compatible with Django ORM and PostgreSQL
