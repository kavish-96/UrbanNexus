from django.db import models

class City(models.Model):
    """
    Master / Dimension table for Cities.
    Using explicit primary key city_id instead of default id.
    """
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.city_name}, {self.state}"

    class Meta:
        managed = True
        db_table = 'city'


class WeatherData(models.Model):
    """
    Daily aggregated weather data per city.
    """
    id = models.BigAutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_logs')
    date = models.DateField()
    temperature = models.FloatField(help_text="Temperature in Celsius")
    humidity = models.FloatField(help_text="Humidity percentage")
    rainfall = models.FloatField(help_text="Rainfall in mm")
    ingested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'weather_data'
        indexes = [
            models.Index(fields=['city', 'date']),
        ]
        # Ensure one weather record per city per day
        unique_together = ('city', 'date')


class AirQuality(models.Model):
    """
    Daily air quality measurements per city.
    """
    id = models.BigAutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='air_quality_logs')
    date = models.DateField()
    aqi = models.SmallIntegerField(help_text="Air Quality Index")
    pm25 = models.FloatField(help_text="PM2.5 concentration")
    pm10 = models.FloatField(help_text="PM10 concentration")
    no2 = models.FloatField(help_text="NO2 concentration")
    ingested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'air_quality'
        indexes = [
            models.Index(fields=['city', 'date']),
        ]
        unique_together = ('city', 'date')


class TrafficData(models.Model):
    """
    Traffic congestion data per city.
    """
    id = models.BigAutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='traffic_logs')
    date = models.DateField()
    traffic_density = models.SmallIntegerField(help_text="Congestion level (1-10)")
    avg_speed = models.FloatField(help_text="Average vehicle speed in km/h")
    ingested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'traffic_data'
        indexes = [
            models.Index(fields=['city', 'date']),
        ]
        unique_together = ('city', 'date')


class AgricultureData(models.Model):
    """
    Agricultural indicators linked to city regions.
    """
    id = models.BigAutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='agriculture_logs')
    date = models.DateField()
    crop_type = models.CharField(max_length=50, help_text="Name of the crop (e.g., Wheat, Rice)")
    yield_amount = models.FloatField(db_column='yield', help_text="Yield in ton/ha") # field renamed because 'yield' is a reserved keyword in Python
    soil_moisture = models.FloatField(help_text="Soil moisture percentage")
    # No ingested_at in provided schema for this table, but assumed good practice? 
    # Adding based on pattern of other tables, or sticking strictly to schema?
    # Schema didn't list it for Agro, so I will OMIT it to be strictly compliant.

    class Meta:
        managed = True
        db_table = 'agriculture_data'
        indexes = [
            models.Index(fields=['city', 'date']),
        ]
        # Unique constraint includes crop_type to allow multiple crops per day per city
        unique_together = ('city', 'date', 'crop_type')


class HealthIndex(models.Model):
    """
    Derived health risk indicators based on environmental factors.
    """
    id = models.BigAutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='health_logs')
    date = models.DateField()
    health_risk_score = models.FloatField(help_text="Risk score 0-100")
    risk_level = models.CharField(max_length=10, help_text="Low / Medium / High")

    class Meta:
        managed = True
        db_table = 'health_index'
        indexes = [
            models.Index(fields=['city', 'date']),
        ]
        unique_together = ('city', 'date')
