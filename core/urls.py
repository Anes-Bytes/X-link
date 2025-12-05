from django.urls import path
from . import views


urlpatterns = [
    # Card Builder and Management
    path('card/builder/', views.card_builder_view, name='card_builder'),
    path('card/success/<int:card_id>/', views.card_success_view, name='card_success'),
    path('card/<str:username>/', views.view_card, name='view_card'),
    
    # AJAX endpoints
    path('api/skill/add/', views.add_skill_ajax, name='add_skill_ajax'),
    path('api/skill/<int:skill_id>/delete/', views.delete_skill_ajax, name='delete_skill_ajax'),
    path('api/card/<int:card_id>/publish/', views.publish_card, name='publish_card'),
]
