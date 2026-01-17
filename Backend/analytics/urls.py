from django.urls import include, path

# urlpatterns = [
#     path("health-risk/<int:city_id>/", HealthRiskComputeView.as_view()),
#     path("api/analytics/", include("analytics_engine.urls")),

# ]


from .views import (
    HealthRiskComputeView,
    HealthRiskForecastView,
    ScenarioSimulationView,
    PolicyRankingView
)

urlpatterns = [
    path("health-risk/<int:city_id>/", HealthRiskComputeView.as_view()),
    path("forecast/<int:city_id>/", HealthRiskForecastView.as_view()),
    path("simulate/<int:city_id>/", ScenarioSimulationView.as_view()),
    path("policies/<int:city_id>/", PolicyRankingView.as_view()),
]
