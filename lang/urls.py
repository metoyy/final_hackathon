from django.urls import path

from category.views import LanguageListView

urlpatterns = [
    path('all/', LanguageListView.as_view()),
]
