from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import RegisterModelViewSet, RegisterView
from django.contrib.auth import views

router = DefaultRouter()
router.register('register', RegisterModelViewSet, basename='register')
urlpatterns = [
    path('', include(router.urls)),
    path('register-form/', RegisterView.as_view(), name='register-form'),
    path('login/', views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
