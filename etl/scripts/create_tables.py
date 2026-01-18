import sys
import os
import logging

# Ensure parent directory is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from db import get_db_cursor

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS city (
            city_id SERIAL PRIMARY KEY,
            city_name VARCHAR(100),
            state VARCHAR(100),
            latitude DECIMAL(9,6),
            longitude DECIMAL(9,6)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS weather_data (
            id BIGSERIAL PRIMARY KEY,
            city_id INT REFERENCES city(city_id),
            date DATE,
            temperature REAL,
            humidity REAL,
            rainfall REAL,
            ingested_at TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS air_quality (
            id BIGSERIAL PRIMARY KEY,
            city_id INT REFERENCES city(city_id),
            date DATE,
            aqi SMALLINT,
            pm25 REAL,
            pm10 REAL,
            no2 REAL,
            ingested_at TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS traffic_data (
            id BIGSERIAL PRIMARY KEY,
            city_id INT REFERENCES city(city_id),
            date DATE,
            traffic_density SMALLINT,
            avg_speed REAL,
            ingested_at TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS agriculture_data (
            id BIGSERIAL PRIMARY KEY,
            city_id INT REFERENCES city(city_id),
            date DATE,
            crop_type VARCHAR(50),
            yield REAL,
            soil_moisture REAL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS health_index (
            id BIGSERIAL PRIMARY KEY,
            city_id INT REFERENCES city(city_id),
            date DATE,
            health_risk_score REAL,
            risk_level VARCHAR(10)
        )
        """
    ]
    
    try:
        with get_db_cursor(commit=True) as cursor:
            for command in commands:
                cursor.execute(command)
        logger.info("All tables created successfully.")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")

if __name__ == "__main__":
    create_tables()
