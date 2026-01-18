import os
import requests
import logging
from django.utils import timezone
from django.conf import settings
from api.models import City, WeatherData

logger = logging.getLogger(__name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_key_here")

def sync_all_cities_weather():
    """
    Fetches live weather for ALL cities in the database
    and updates the WeatherData table.
    """
    cities = City.objects.all()
    results = {"success": [], "failed": []}

    for city in cities:
        try:
            # 1. Fetch from OpenWeatherMap
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': city.latitude,
                'lon': city.longitude,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            # 2. Parse Data
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            # OWM puts rain in 'rain' object usually, defaulting to 0
            rainfall = data.get('rain', {}).get('1h', 0)

            # 3. Save to DB (Update or Create for Today)
            # We want to capture the latest "Snapshot" as today's record
            today = timezone.now().date()
            
            obj, created = WeatherData.objects.update_or_create(
                city=city,
                date=today,
                defaults={
                    'temperature': temp,
                    'humidity': humidity,
                    'rainfall': rainfall
                }
            )

            
            # 4. Trigger Risk Re-calculation
            try:
                from analytics.services.risk_engine import trigger_risk_calculation
                trigger_risk_calculation(city)
            except ImportError:
                # If module not ready, skip
                pass
            except Exception as e:
                logger.error(f"Risk calculation failed for {city.city_name}: {e}")

            action = "Created" if created else "Updated"
            results["success"].append(f"{city.city_name}: {action} (T:{temp}C, R:{rainfall}mm)")

        except Exception as e:
            logger.error(f"Failed to sync {city.city_name}: {e}")
            results["failed"].append(f"{city.city_name}: {str(e)}")

    return results
