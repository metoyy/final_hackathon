from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.CategoryListView.as_view()),
    path('<int:pk>/', views.CategoryDetailView.as_view()),
]