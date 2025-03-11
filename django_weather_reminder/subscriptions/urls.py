from django.urls import include, path
from rest_framework.routers import DefaultRouter

from subscriptions.views import (CityViewSet, SubscriptionViewSet,
                                 TriggerNotificationsView,
                                 UpdateWeatherDataView, IndexView, DeleteSubscriptionView)

router = DefaultRouter()
router.register('cities', CityViewSet)
router.register('subscriptions', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('', include(router.urls)),
    path('trigger-notifications/', TriggerNotificationsView.as_view(), name='trigger-notifications'),
    path('update-weather/', UpdateWeatherDataView.as_view(), name='update-weather'),
    path('delete_subscription/', DeleteSubscriptionView.as_view(), name='delete-subscription'),
]
