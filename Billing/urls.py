from django.urls import path
from . import views

urlpatterns = [
    # Card Builder and Management
    path('', views.landing_view, name='home'),
    path('payment_success/', views.payment_success_view, name='payment_success'),
    path('payment-failed/', views.payment_failed_view, name='payment_failed'),
    path('buy-telegram/', views.buy_telegram_view, name='buy_telegram'),
    path('x/', views.about_view, name='about'),
]
