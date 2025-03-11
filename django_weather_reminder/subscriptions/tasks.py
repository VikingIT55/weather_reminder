import logging
from abc import ABC, abstractmethod

from celery import shared_task
from django.db import DatabaseError
from django.utils import timezone

from subscriptions.models import Subscription
from subscriptions.notifications import (send_email_notification,
                                         send_webhook_notification)
from weather_api.models import WeatherData

logger = logging.getLogger(__name__)

class DeliveryMethod(ABC):
    @abstractmethod
    def send(self, subscription, message):
        pass


class EmailDelivery(DeliveryMethod):
    def send(self, subscription, message):
        text_message = (
            f"Погода в місті {subscription.city.name}:\n"
            f"Температура: {message['temperature']}°C\n"
            f"Умови: {message['conditions']}\n"
            f"Вологість: {message['humidity']}%\n"
        )
        send_email_notification(
            to_email=subscription.user.email,
            subject=F"Сповіщення про погоду: {subscription.city.name}",
            message=text_message,
        )


class WebhookDelivery(DeliveryMethod):
    def send(self, subscription, message):
        payload = {
            "city": subscription.city.name,
            "temperature": message['temperature'],
            "conditions": message['conditions'],
            "humidity": message['humidity'],
        }
        send_webhook_notification(subscription.webhook_url, payload)


class NotificationManager:
    DELIVERY_METHOD = {
        'email': EmailDelivery(),
        'webhook': WebhookDelivery(),
    }

    def send_notification(self, subscription, message):
        delivery_method = self.DELIVERY_METHOD.get(subscription.delivery_method)
        if delivery_method:
            delivery_method.send(subscription, message)
        else:
            logger.error(f"Unsupported delivery method: {subscription.delivery_method}")

def prepare_notification(city_id=None, user_id=None):
    if city_id:
        return Subscription.objects.filter(city=city_id)
    elif user_id:
        return Subscription.objects.filter(user=user_id)
    return Subscription.objects.all()

def check_notification_is_valid(subscription):
    weather = WeatherData.objects.filter(city=subscription.city).order_by('-timestamp').first()
    if not weather:
        logger.warning(f"No weather records found for city {subscription.city} (Subscription ID: {subscription.id}).")
        return None

    return {
        "temperature": weather.temperature,
        "conditions": weather.conditions,
        "humidity": weather.humidity,
    }


def send_notification(subscription, message, manager, now):
    try:
        subscription.last_notified = now
        subscription.save()
    except DatabaseError as db_err:
        logger.error(f"Failed to save subscription (ID: {subscription.id}) to DB: {db_err}")
        return
    except Exception as e:
        logger.error(f"Unexpected error while saving subscription (ID: {subscription.id}): {e}")
        return
    manager.send_notification(subscription, message)

@shared_task
def send_notifications(city_id=None, user_id=None):
    subscriptions = prepare_notification(city_id, user_id)
    now = timezone.now()
    manager = NotificationManager()

    for subscription in subscriptions:
        message = check_notification_is_valid(subscription)
        if message:
            send_notification(subscription, message, manager, now)
