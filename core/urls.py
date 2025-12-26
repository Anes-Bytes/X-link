from django.urls import path
from . import views

urlpatterns = [
    # Card Builder and Management
    path('register', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("dashboard", views.dashboard_view, name='dashboard'),
    path("request-otp/", views.request_otp, name="request_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
]
