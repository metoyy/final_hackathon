from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.UserListApiView.as_view()),
    path('register/', views.RegistrationView.as_view()),
    path('activate/', views.ActivationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('password_reset/', views.PasswordResetView.as_view()),
    path('logout/', LogoutView.as_view()),
]