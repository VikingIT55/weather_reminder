import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from subscriptions.models import City
from weather_api.models import WeatherData


class WeatherAlertTestCase(APITestCase):

    def setUp(self):
        self.city = City.objects.create(name='Kyiv')
        self.url = reverse('weather_api:weather-alert')
        self.valid_payload = {
            'city': self.city.id,
            'temperature': 10,
            'conditions': 'clear sky',
            'humidity': 60,
        }
        self.user = self.setup_user()
        self.client.force_authenticate(user=self.user)

    def setup_user(self):
        User = get_user_model()
        return User.objects.create_user(username='testuser', password='PASSWORD')

    @patch("subscriptions.tasks.send_notifications.delay")
    def test_create_weather_alert_triggest_celery_task(self, mock_celery_task):
        WeatherData.objects.create(city=self.city, temperature=5,conditions="cloudy", humidity=60)
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_celery_task.assert_called_once()
