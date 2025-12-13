from django.urls import path
from . import views



urlpatterns = [
    # Card Builder and Management
    path('', views.landing_view, name='home'),
    path('payment_success/', views.payment_success_view, name='payment_success'),
    path('payment-failed/', views.payment_failed_view, name='payment_failed'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('card/builder/', views.card_builder_view, name='card_builder'),
    path('card/success/<int:card_id>/', views.card_success_view, name='card_success'),
    path('register', views.login_view, name='login'),
    path("dashboard", views.dashboard_view, name='dashboard'),
    path('<str:username>', views.view_card, name='view_card'),
    path("request-otp/", views.request_otp, name="request_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),


    # AJAX endpoints
    path('api/skill/add/', views.add_skill_ajax, name='add_skill_ajax'),
    path('api/skill/<int:skill_id>/delete/', views.delete_skill_ajax, name='delete_skill_ajax'),

]
