from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from . import views


urlpatterns = [
    path('', views.UserListApiView.as_view()),
    path('register/', views.RegistrationView.as_view()),
    path('activate/', views.ActivationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('password_reset/', views.PasswordResetView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('login-success/', views.LoginSuccess.as_view()),
    path('blacklist/', TokenBlacklistView.as_view()),
]