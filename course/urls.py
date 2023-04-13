
from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.CoursesViewSet)
urlpatterns = [
    path('', include(router.urls)),
]