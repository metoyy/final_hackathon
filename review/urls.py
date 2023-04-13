from review import views
from django.urls import path
urlpatterns = [
    path('', views.ReviewCreateView.as_view()),
    path('<int:pk>/', views.ReviewDetailView.as_view()),
]