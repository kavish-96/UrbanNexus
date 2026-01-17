from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CityViewSet, WeatherViewSet, AirQualityViewSet, 
    TrafficViewSet, AgricultureViewSet, HealthIndexViewSet,
    CityDashboardView
)

router = DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'weather', WeatherViewSet)
router.register(r'air-quality', AirQualityViewSet)
router.register(r'traffic', TrafficViewSet)
router.register(r'agriculture', AgricultureViewSet)
router.register(r'health', HealthIndexViewSet)

urlpatterns = [
    # Router URLs (Standard CRUD)
    path('', include(router.urls)),
    
    # Custom Analytics URLs
    path('dashboard/', CityDashboardView.as_view(), name='city-dashboard'),
]
