from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from subscriptions.models import City, Subscription
from subscriptions.serializers import CitySerializer, SubscriptionSerializer
from subscriptions.tasks import send_notifications
from weather_api.tasks import update_weather_data


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Subscription.objects.none()
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TriggerNotificationsView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        send_notifications.delay(user_id=request.user.id)
        return Response({"message": "Notifications triggered!"})


class UpdateWeatherDataView(APIView):
    def get(self, request):
        update_weather_data.delay()
        return Response({"message": "Weather data update triggered!"})

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.all()
        context["subscriptions"] = Subscription.objects.filter(user=self.request.user)
        delivery_method_field = Subscription._meta.get_field('delivery_method')
        context["delivery_method"] = delivery_method_field.choices
        return context

class DeleteSubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        if request.data.get('_method') == 'DELETE':
            sub_id = request.data.get('sub_id') or request.POST.get('sub_id')
            print(sub_id)
            try:
                subscription = Subscription.objects.get(id=sub_id)
                subscription.delete()
                return Response({"message": "Subscription deleted."}, status=status.HTTP_204_NO_CONTENT)
            except Subscription.DoesNotExist:
                return Response({"error": "Subscription not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Invalid method."}, status=status.HTTP_400_BAD_REQUEST)
