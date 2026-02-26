from django.urls import path

from . import views

urlpatterns = [
    path("shop/<int:shop_id>/", views.shop_view, name="shop_view"),
    path("shops/create/", views.create_shop_view, name="shop_create"),
    path("shops/<int:shop_id>/manage/", views.manage_shop_view, name="shop_manage"),
    path("shops/<int:shop_id>/delete/", views.delete_shop_view, name="shop_delete"),
]
