from datetime import datetime, timezone
from etl.db import get_db_cursor
import logging

logger = logging.getLogger(__name__)

class Loader:
    _city_cache = {}

    @classmethod
    def get_city_id(cls, city_name):
        if city_name in cls._city_cache:
            return cls._city_cache[city_name]

        with get_db_cursor(commit=True) as cursor:
            # Try to find city
            cursor.execute("SELECT city_id FROM city WHERE city_name = %s", (city_name,))
            res = cursor.fetchone()
            if res:
                cls._city_cache[city_name] = res[0]
                return res[0]
            
            # If not found, insert
            # Default lat/lon for Delhi if not provided?
            # Prompt says "Delhi (India) ONLY".
            # We insert with defaults if needed.
            lat, lon = 28.7041, 77.1025 # Default Delhi coordinates
            cursor.execute(
                "INSERT INTO city (city_name, state, latitude, longitude) VALUES (%s, %s, %s, %s) RETURNING city_id",
                (city_name, 'Delhi', lat, lon)
            )
            city_id = cursor.fetchone()[0]
            cls._city_cache[city_name] = city_id
            logger.info(f"Created new city: {city_name} (ID: {city_id})")
            return city_id

    @staticmethod
    def load_weather_data(records):
        inserted_count = 0
        with get_db_cursor(commit=True) as cursor:
            for record in records:
                if not record: continue
                city_id = Loader.get_city_id(record['city_name'])
                ingested_at = datetime.now(timezone.utc)
                
                cursor.execute("""
                    INSERT INTO weather_data (city_id, date, temperature, humidity, rainfall, ingested_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (city_id, record['date'], record['temperature'], record['humidity'], record['rainfall'], ingested_at))
                inserted_count += 1
        return inserted_count

    @staticmethod
    def load_aqi_data(records):
        inserted_count = 0
        with get_db_cursor(commit=True) as cursor:
            for record in records:
                if not record: continue
                city_id = Loader.get_city_id(record['city_name'])
                ingested_at = datetime.now(timezone.utc)
                
                cursor.execute("""
                    INSERT INTO air_quality (city_id, date, aqi, pm25, pm10, no2, ingested_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (city_id, record['date'], record['aqi'], record['pm25'], record['pm10'], record['no2'], ingested_at))
                inserted_count += 1
        return inserted_count

    @staticmethod
    def load_traffic_data(records):
        inserted_count = 0
        with get_db_cursor(commit=True) as cursor:
            for record in records:
                if not record: continue
                city_id = Loader.get_city_id(record['city_name'])
                ingested_at = datetime.now(timezone.utc)
                
                cursor.execute("""
                    INSERT INTO traffic_data (city_id, date, traffic_density, avg_speed, ingested_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (city_id, record['date'], record['traffic_density'], record['avg_speed'], ingested_at))
                inserted_count += 1
        return inserted_count

    @staticmethod
    def load_agriculture_data(records):
        inserted_count = 0
        with get_db_cursor(commit=True) as cursor:
            for record in records:
                if not record: continue
                city_id = Loader.get_city_id(record['city_name'])
                
                cursor.execute("""
                    INSERT INTO agriculture_data (city_id, date, crop_type, yield, soil_moisture)
                    VALUES (%s, %s, %s, %s, %s)
                """, (city_id, record['date'], record['crop_type'], record['yield'], record['soil_moisture']))
                inserted_count += 1
        return inserted_count

    @staticmethod
    def load_health_data(records):
        inserted_count = 0
        with get_db_cursor(commit=True) as cursor:
            for record in records:
                if not record: continue
                city_id = Loader.get_city_id(record['city_name'])
                
                cursor.execute("""
                    INSERT INTO health_index (city_id, date, health_risk_score, risk_level)
                    VALUES (%s, %s, %s, %s)
                """, (city_id, record['date'], record['health_risk_score'], record['risk_level']))
                inserted_count += 1
        return inserted_count
