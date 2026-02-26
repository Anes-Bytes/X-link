from django.urls import path

from cards.views import view_card_by_subdomain


urlpatterns = [
    path("", view_card_by_subdomain, name="subdomain_public_page"),
]
