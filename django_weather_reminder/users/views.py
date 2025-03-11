from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.views.generic import TemplateView

from users.models import User
from users.serializers import RegisterSerializer


class RegisterModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class RegisterView(TemplateView):
    template_name = "register.html"
