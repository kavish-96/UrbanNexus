import logging
from api.models import City, WeatherData, AirQuality, TrafficData, AgricultureData, HealthIndex
from analytics.services.health_risk import compute_health_risk
from django.utils import timezone

logger = logging.getLogger(__name__)

def trigger_risk_calculation(city):
    """
    Called after any data ingestion (Weather, AQI, Traffic sync).
    Re-calculates the Health Risk Score for the city and saves it.
    """
    try:
        # Get latest available data snippet
        today = timezone.now().date()
        
        weather = WeatherData.objects.filter(city=city).order_by('-date').first()
        air = AirQuality.objects.filter(city=city).order_by('-date').first()
        traffic = TrafficData.objects.filter(city=city).order_by('-date').first()
        agri = AgricultureData.objects.filter(city=city).order_by('-date').first()

        # If we miss critical data, use defaults or skip
        if not weather or not air or not traffic:
             logger.warning(f"Skipping risk calc for {city.city_name}: Missing core data.")
             return

        # Use the imported calculation logic
        score, level = compute_health_risk(weather, air, agri, traffic)
        
        # Save Result
        HealthIndex.objects.update_or_create(
            city=city,
            date=today,
            defaults={
                'health_risk_score': score,
                'risk_level': level
            }
        )
        logger.info(f"Risk Updated for {city.city_name}: {score} ({level})")

    except Exception as e:
        logger.error(f"Error calculating risk for {city.city_name}: {e}")
