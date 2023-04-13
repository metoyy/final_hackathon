
from django.urls import path, include
from . import views
from like.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.CoursesViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/add_fav/', views.FavoriteAddOrDeletePost.as_view()),
    path('<int:pk>/like/', LikeCreateDeleteView.as_view()),
]