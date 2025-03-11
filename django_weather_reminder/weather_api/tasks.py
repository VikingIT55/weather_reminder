from celery import shared_task

from subscriptions.models import City
from weather_api.models import WeatherData
from weather_api.services import fetch_weather


@shared_task
def update_weather_data():
    cities = City.objects.all()
    for city in cities:
        weather = fetch_weather(city.name)
        if weather:
            WeatherData.objects.create(
                city=city,
                temperature=weather['temperature'],
                conditions=weather['conditions'],
                humidity=weather['humidity']
            )
