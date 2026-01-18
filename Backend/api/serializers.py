from rest_framework import serializers
from .models import City, WeatherData, AirQuality, TrafficData, AgricultureData, HealthIndex

class CitySerializer(serializers.ModelSerializer):
    current_risk = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = '__all__'

    def get_current_risk(self, obj):
        latest_health = obj.health_logs.order_by('-date').first()
        return latest_health.risk_level if latest_health else "Unknown"

class WeatherDataSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.city_name')
    
    class Meta:
        model = WeatherData
        fields = '__all__'

class AirQualitySerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.city_name')

    class Meta:
        model = AirQuality
        fields = '__all__'

class TrafficDataSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.city_name')

    class Meta:
        model = TrafficData
        fields = '__all__'

class AgricultureDataSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.city_name')

    class Meta:
        model = AgricultureData
        fields = '__all__'

class HealthIndexSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.city_name')

    class Meta:
        model = HealthIndex
        fields = '__all__'
