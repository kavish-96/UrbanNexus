from datetime import datetime
import logging
from dateutil.parser import parse

logger = logging.getLogger(__name__)

class Transformer:
    @staticmethod
    def clean_float(value, default=0.0):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def clean_int(value, default=0):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def normalize_date(date_str):
        """
        Normalize various date formats to YYYY-MM-DD.
        """
        if not date_str:
            return None
        try:
            return parse(str(date_str)).date()
        except Exception:
            logger.warning(f"Could not parse date: {date_str}")
            return None

    @staticmethod
    def transform_weather_csv(record):
        date_val = Transformer.normalize_date(record.get('date'))
        temperature = Transformer.clean_float(record.get('temperature'))
        humidity = Transformer.clean_float(record.get('humidity'))
        rainfall = Transformer.clean_float(record.get('rainfall'))

        if not (-5 <= temperature <= 50):
            logger.warning(f"Dropped weather row (temp): {temperature}")
            return None

        if not (0 <= humidity <= 100):
            logger.warning(f"Dropped weather row (humidity): {humidity}")
            return None

        if rainfall < 0:
            logger.warning(f"Dropped weather row (rainfall): {rainfall}")
            return None

        return {
            'city_name': record.get('city', 'Delhi'),
            'date': date_val,
            'temperature': temperature,
            'humidity': humidity,
            'rainfall': rainfall,
        }

    @staticmethod
    def transform_weather_api(data):
        # OpenWeatherMap API transformation
        # Needs to handle missing keys gracefully
        try:
            # Convert unix timestamp to date
            dt_ts = data.get('dt')
            date_val = datetime.fromtimestamp(dt_ts).date() if dt_ts else datetime.today().date()
            
            main = data.get('main', {})
            rain = data.get('rain', {})
            
            # City name might be specific (e.g. Pitampura), but we might want to map it to Delhi 
            # if we are tracking Delhi as a whole. Ideally we use the returned name.
            # But per prompt "City Focus: Delhi". Let's stick to what API gives or normalize if needed.
            # For now, use the API name, but normalize 'Pitampura' to 'Delhi' ?? 
            # The prompt says "City: Delhi (India) ONLY". 
            # I will force 'Delhi' if the API response coordinates are within Delhi,
            # or just assume the Config API call is for Delhi.
            # Let's use 'Delhi' to ensure it links to the main city entry.
            
            return {
                'city_name': 'Delhi', 
                'date': date_val,
                'temperature': Transformer.clean_float(main.get('temp')),
                'humidity': Transformer.clean_float(main.get('humidity')),
                'rainfall': Transformer.clean_float(rain.get('1h', 0.0)), # rain 1h volume
            }
        except Exception as e:
            logger.error(f"Error transforming API weather data: {e}")
            return None

    @staticmethod
    def transform_aqi_csv(record):
        aqi = Transformer.clean_int(record.get('aqi'))
        pm25 = Transformer.clean_float(record.get('pm25'))
        pm10 = Transformer.clean_float(record.get('pm10'))
        no2 = Transformer.clean_float(record.get('no2'))

        if aqi < 0 or pm25 < 0 or pm10 < pm25 or no2 <= 0:
            logger.warning(f"Dropped AQI row: {record}")
            return None

        return {
            'city_name': record.get('city', 'Delhi'),
            'date': Transformer.normalize_date(record.get('date')),
            'aqi': aqi,
            'pm25': pm25,
            'pm10': pm10,
            'no2': no2,
        }

    @staticmethod
    def transform_traffic_csv(record):
        density = Transformer.clean_int(record.get('traffic_density'))
        speed = Transformer.clean_float(record.get('avg_speed'))

        if not (1 <= density <= 10):
            return None

        if not (5 <= speed <= 60):
            return None

        return {
            'city_name': record.get('city', 'Delhi'),
            'date': Transformer.normalize_date(record.get('date')),
            'traffic_density': density,
            'avg_speed': speed,
        }

    @staticmethod
    def transform_agriculture_csv(record):
        # city,date,crop_type,yield,soil_moisture,rainfall
        return {
            'city_name': record.get('city', 'Delhi'),
            'date': Transformer.normalize_date(record.get('date')),
            'crop_type': record.get('crop_type', 'Unknown'),
            'yield': Transformer.clean_float(record.get('yield')),
            'soil_moisture': Transformer.clean_float(record.get('soil_moisture')),
        }

    @staticmethod
    def transform_agriculture_json(record):
        # Assume JSON structure similar to CSV or flat
        # Or if it matches the schema directly.
        # User didn't give JSON schema, but said "optional alternative".
        # I'll assume keys match DB columns or CSV headers.
        return {
            'city_name': record.get('city', 'Delhi'),
            'date': Transformer.normalize_date(record.get('date')),
            'crop_type': record.get('crop_type', 'Unknown'),
            'yield': Transformer.clean_float(record.get('yield')),
            'soil_moisture': Transformer.clean_float(record.get('soil_moisture')),
        }

    @staticmethod
    def transform_health_csv(record):
        score = Transformer.clean_float(record.get('health_risk_score'))

        if not (0 <= score <= 100):
            return None

        risk = record.get('risk_level', 'Low')
        if risk not in ('Low', 'Medium', 'High'):
            risk = 'Low'

        return {
            'city_name': record.get('city', 'Delhi'),
            'date': Transformer.normalize_date(record.get('date')),
            'health_risk_score': score,
            'risk_level': risk,
        }

