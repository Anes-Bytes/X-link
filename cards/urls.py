from django.urls import path
from . import views

urlpatterns = [
    # Card Builder and Management
    path('card/builder/', views.card_builder_view, name='card_builder'),
    path('card/success/<int:card_id>/', views.card_success_view, name='card_success'),
    path('<str:username>', views.view_card, name='view_card'),


    # AJAX endpoints
    path('api/skill/add/', views.add_skill_ajax, name='add_skill_ajax'),
    path('api/skill/<int:skill_id>/delete/', views.delete_skill_ajax, name='delete_skill_ajax'),
    path('api/service/add/', views.add_service_ajax, name='add_service_ajax'),
    path('api/service/<int:service_id>/delete/', views.delete_service_ajax, name='delete_service_ajax'),
    path('api/portfolio/<int:portfolio_id>/delete/', views.delete_portfolio_ajax, name='delete_portfolio_ajax'),

]
