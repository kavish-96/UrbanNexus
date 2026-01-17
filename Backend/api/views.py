from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Max, Min

from .models import City, WeatherData, AirQuality, TrafficData, AgricultureData, HealthIndex
from .serializers import (
    CitySerializer, WeatherDataSerializer, AirQualitySerializer, 
    TrafficDataSerializer, AgricultureDataSerializer, HealthIndexSerializer
)

# --- Standard CRUD APIs ---

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class WeatherViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all().order_by('-date')
    serializer_class = WeatherDataSerializer
    filterset_fields = ['city', 'date'] # Requires django-filter, sticking to basic for now

    def get_queryset(self):
        """Allow filtering by city_id via query param"""
        queryset = super().get_queryset()
        city_id = self.request.query_params.get('city_id')
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset

class AirQualityViewSet(viewsets.ModelViewSet):
    queryset = AirQuality.objects.all().order_by('-date')
    serializer_class = AirQualitySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        city_id = self.request.query_params.get('city_id')
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset

class TrafficViewSet(viewsets.ModelViewSet):
    queryset = TrafficData.objects.all().order_by('-date')
    serializer_class = TrafficDataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        city_id = self.request.query_params.get('city_id')
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset

class AgricultureViewSet(viewsets.ModelViewSet):
    queryset = AgricultureData.objects.all().order_by('-date')
    serializer_class = AgricultureDataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        city_id = self.request.query_params.get('city_id')
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset

class HealthIndexViewSet(viewsets.ModelViewSet):
    queryset = HealthIndex.objects.all().order_by('-date')
    serializer_class = HealthIndexSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        city_id = self.request.query_params.get('city_id')
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset


# --- Analytics / Dashboard APIs (The 'Brain') ---

class CityDashboardView(APIView):
    """
    Returns a snapshot of the latest data for a specific city.
    Usage: /api/dashboard/?city_id=1
    """
    def get(self, request):
        city_id = request.query_params.get('city_id')
        if not city_id:
            return Response({"error": "city_id parameter is required"}, status=400)
        
        city = get_object_or_404(City, pk=city_id)
        
        # Helper to get latest record
        def get_latest(model):
            return model.objects.filter(city=city).order_by('-date').first()

        weather = get_latest(WeatherData)
        aqi = get_latest(AirQuality)
        traffic = get_latest(TrafficData)
        health = get_latest(HealthIndex)
        agro = AgricultureData.objects.filter(city=city).order_by('-date')[:5] # Last 5 Agro records

        data = {
            "city": city.city_name,
            "state": city.state,
            "latest_stats": {
                "temperature": weather.temperature if weather else None,
                "humidity": weather.humidity if weather else None,
                "aqi": aqi.aqi if aqi else None,
                "pm25": aqi.pm25 if aqi else None,
                "traffic_density": traffic.traffic_density if traffic else None,
                "health_risk": health.health_risk_score if health else None,
                "risk_level": health.risk_level if health else None,
            },
            "recent_crops": AgricultureDataSerializer(agro, many=True).data
        }
        return Response(data)
