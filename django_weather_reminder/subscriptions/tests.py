from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from subscriptions.models import City, Subscription
from subscriptions.tasks import NotificationManager, send_notifications
from weather_api.models import WeatherData


class SendNotificationsTaskTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='PASSWORD')
        self.city = City.objects.create(name="Kyiv")
        self.weather = WeatherData.objects.create(
            city=self.city, temperature=10, conditions="clear sky", humidity=60
        )
        self.subscription = Subscription.objects.create(
            user=self.user, city=self.city, delivery_method="email", last_notified=None
        )

    @patch("subscriptions.tasks.EmailDelivery.send")
    def test_send_notifications_email(self, mock_email):
        send_notifications()
        mock_email.assert_called_once()


class NotificationDeliveryTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='PASSWORD')
        self.city = City.objects.create(name="Kyiv")
        self.subscription = Subscription.objects.create(
            user=self.user, city=self.city, delivery_method="email", last_notified=None
        )
        self.message = {"temperature": 5, "conditions": "cloudy", "humidity": 50}

    @patch("subscriptions.tasks.EmailDelivery.send")
    def test_email_delivery(self, mock_send_email):
        manager = NotificationManager()
        manager.send_notification(self.subscription, self.message)
        mock_send_email.assert_called_once()

    @patch("subscriptions.tasks.WebhookDelivery.send")
    def test_webhook_delivery(self, mock_send_webhook):
        self.subscription.delivery_method = "webhook"
        self.subscription.webhook_url ="https://example.com"
        manager = NotificationManager()
        manager.send_notification(self.subscription, self.message)
        mock_send_webhook.assert_called_once()
