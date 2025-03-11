from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from subscriptions.tasks import send_notifications
from weather_api.serializers import WeatherDataSerializer


class WeatherAlertView(APIView):
    def post(self, request):
        serializer = WeatherDataSerializer(data=request.data)
        if serializer.is_valid():
            weather_data = serializer.save()
            send_notifications.delay(weather_data.city.id)
            return Response(
                        {"detail": "New entry saved, notification sent."},
                        status=status.HTTP_201_CREATED
                    )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
