import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_reminder.settings')
app = Celery('weather_reminder')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'update-weather-data-every-hour': {
        'task': 'weather_api.tasks.update_weather_data',
        'schedule': 3600.0,  # every hour
    },
    'send-weather-notifications': {
        'task': 'subscriptions.tasks.send_notifications',
        'schedule': 3600.0,  # every hour
    }
}

app.conf.broker_connection_retry_on_startup = True

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
