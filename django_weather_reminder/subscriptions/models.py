from enum import Enum

from django.conf import settings
from django.db import models
from django_enum_choices.choice_builders import value_value
from django_enum_choices.fields import EnumChoiceField


class City(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - {self.country_code}"


class PeriodEnum(Enum):
    ONE = 1
    THREE = 3
    SIX = 6
    TWELVE = 12

    def to_hours(self):
        return self.value


class CustomEnumChoiceField(EnumChoiceField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.enum_class(int(value))

    def get_prep_value(self, value):
        if isinstance(value, self.enum_class):
            return str(value.value)
        return value


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    period = CustomEnumChoiceField(PeriodEnum, default=PeriodEnum.ONE, choice_builder=value_value)
    delivery_method = models.CharField(max_length=100, choices=[('email', 'Email'), ('webhook', 'Webhook')])
    webhook_url = models.URLField(blank=True, null=True)
    last_notified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.city.name} - {self.period}"
