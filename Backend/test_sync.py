
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from api.services.weather_sync import sync_all_cities_weather

print(f"API Key present: {bool(os.getenv('OPENWEATHER_API_KEY'))}")
print("Starting Sync...")
result = sync_all_cities_weather()
print("Sync Result:", result)
