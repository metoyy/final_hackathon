from django.urls import path

from mentors.views import MentorsListCreateView

urlpatterns = [
    path('', MentorsListCreateView.as_view()),
]
