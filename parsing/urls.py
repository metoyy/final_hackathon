from django.urls import path

from parsing import views

urlpatterns = [
    path('courses/', views.AllCoursesView.as_view()),
    path('calls/', views.LeaveNumberView.as_view()),
    path('accounts/', views.AllAccountsView.as_view()),
    path('addaccount/', views.AddAccountView.as_view()),
    path('accountdetails/<str:pk>/', views.AccountDetails.as_view()),
    path('checkview/', views.CheckView.as_view()),
]
