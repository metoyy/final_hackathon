from review.views import CourseReviewListView
from django.urls import path, include
from . import views
from like.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.CoursesViewSet)

urlpatterns = [
    path('<int:pk>/add_fav/', views.FavoriteAddOrDeletePost.as_view()),
    path('<int:pk>/like/', LikeCreateDeleteView.as_view()),
    path('<int:pk>/reviews/', CourseReviewListView.as_view()),
    path('favorites/', views.FavoriteCourseListView.as_view()),
    path('featured/', views.FeaturedCoursesView.as_view()),
    path('<int:pk>/purchase/', views.PurchaseCreateView.as_view()), #post - to purchase, put - to confirm purchase
    path('mycourses/', views.PurchaseListView.as_view()),
    path('', include(router.urls)),

]
