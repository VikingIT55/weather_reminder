from django.urls import path

from .views import WeatherAlertView

urlpatterns = [
    path('weather-alert/', WeatherAlertView.as_view(), name='weather-alert'),
]
