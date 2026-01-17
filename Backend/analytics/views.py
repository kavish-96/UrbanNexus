from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from api.models import (
    City, WeatherData, AirQuality,
    AgricultureData, TrafficData, HealthIndex
)

from analytics.services.health_risk import compute_health_risk
from analytics.services.urban_forecast import load_model, predict_risk
from analytics.services.scenario_engine import simulate_scenario
from analytics.services.policy_ranker import rank_policies




class HealthRiskComputeView(APIView):

    def post(self, request, city_id):
        city = City.objects.get(city_id=city_id)

        weather = WeatherData.objects.filter(city=city).latest("date")
        air = AirQuality.objects.filter(city=city).latest("date")
        agri = AgricultureData.objects.filter(city=city).latest("date")
        traffic = TrafficData.objects.filter(city=city).latest("date")

        score, level = compute_health_risk(weather, air, agri, traffic)

        record = HealthIndex.objects.create(
            city=city,
            date=timezone.now().date(),
            health_risk_score=score,
            risk_level=level
        )

        return Response({
            "city": city.city_name,
            "health_risk_score": score,
            "risk_level": level
        })
        
        
class HealthRiskForecastView(APIView):

    def get(self, request, city_id):

        city = City.objects.get(city_id=city_id)

        weather = WeatherData.objects.filter(city=city).latest("date")
        air = AirQuality.objects.filter(city=city).latest("date")
        agri = AgricultureData.objects.filter(city=city).latest("date")
        traffic = TrafficData.objects.filter(city=city).latest("date")

        model = load_model()

        features = {
            "aqi": air.aqi,
            "temperature": weather.temperature,
            "humidity": weather.humidity,
            "rainfall": weather.rainfall,
            "traffic_density": traffic.traffic_density,
            "yield": agri.yeild,
        }

        day3 = predict_risk(model, features)
        day7 = predict_risk(model, features)

        return Response({
            "city": city.city_name,
            "current_risk": features,
            "day_3_prediction": day3,
            "day_7_prediction": day7
        })


class ScenarioSimulationView(APIView):

    def post(self, request, city_id):

        city = City.objects.get(city_id=city_id)

        weather = WeatherData.objects.filter(city=city).latest("date")
        air = AirQuality.objects.filter(city=city).latest("date")
        agri = AgricultureData.objects.filter(city=city).latest("date")
        traffic = TrafficData.objects.filter(city=city).latest("date")

        scenario = request.data

        new_score, level = simulate_scenario(
            weather, air, agri, traffic, scenario
        )

        return Response({
            "city": city.city_name,
            "simulated_risk_score": new_score,
            "risk_level": level
        })


class PolicyRankingView(APIView):

    def get(self, request, city_id):

        city = City.objects.get(city_id=city_id)

        weather = WeatherData.objects.filter(city=city).latest("date")
        air = AirQuality.objects.filter(city=city).latest("date")
        agri = AgricultureData.objects.filter(city=city).latest("date")
        traffic = TrafficData.objects.filter(city=city).latest("date")

        ranking = rank_policies(weather, air, agri, traffic)

        return Response({
            "city": city.city_name,
            "policy_ranking": ranking
        })
