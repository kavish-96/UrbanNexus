from rest_framework import serializers
from .models import City, WeatherData, AirQuality, TrafficData, AgricultureData, HealthIndex

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

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
