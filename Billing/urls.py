from django.urls import path
from . import views

urlpatterns = [
    # Card Builder and Management
    path('', views.landing_view, name='home'),
    path('payment_success/', views.payment_success_view, name='payment_success'),
    path('payment-failed/', views.payment_failed_view, name='payment_failed'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('telegram-checkout/', views.telegram_checkout_view, name='telegram_checkout'),
    path('x/', views.about_view, name='about'),
]
