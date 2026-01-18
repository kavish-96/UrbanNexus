
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from api.models import WeatherData
from django.utils import timezone

logs = WeatherData.objects.filter(date=timezone.now().date())
print(f"{'City':<15} | {'Ingested At (UTC)'}")
print("-" * 35)
for log in logs:
    city_name = log.city.city_name
    # Shows the exact time stored in DB
    updated_at = log.ingested_at.strftime("%H:%M:%S") 
    print(f"{city_name:<15} | {updated_at}")
