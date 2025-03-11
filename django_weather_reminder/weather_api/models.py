from django.db import models


class WeatherData(models.Model):
    city = models.ForeignKey('subscriptions.City', on_delete=models.CASCADE)
    temperature = models.FloatField()
    conditions = models.CharField(max_length=255)
    humidity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city.name} - {self.temperature}°C"
