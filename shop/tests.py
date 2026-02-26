from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Product, UserShop


class ShopModelTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="shopuser",
            password="StrongPass123",
            full_name="Shop User",
        )
        self.shop = UserShop.objects.create(
            user=self.user,
            name="My Shop",
            logo=SimpleUploadedFile("logo.png", b"logo_content", content_type="image/png"),
        )

    def test_final_price_is_computed(self):
        product = Product.objects.create(
            shop=self.shop,
            name="Product A",
            image=SimpleUploadedFile("p.png", b"img", content_type="image/png"),
            short_description="Desc",
            price=100000,
            discount_percent=25,
            is_active=True,
        )
        self.assertEqual(float(product.final_price), 75000.00)


class ShopViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="shopuser2",
            password="StrongPass123",
            full_name="Shop User",
        )
        self.shop = UserShop.objects.create(
            user=self.user,
            name="My Shop",
            logo=SimpleUploadedFile("logo.png", b"logo_content", content_type="image/png"),
        )
        Product.objects.create(
            shop=self.shop,
            name="Visible Product",
            image=SimpleUploadedFile("p1.png", b"img", content_type="image/png"),
            short_description="Visible",
            price=50000,
            discount_percent=10,
            is_active=True,
        )
        Product.objects.create(
            shop=self.shop,
            name="Hidden Product",
            image=SimpleUploadedFile("p2.png", b"img", content_type="image/png"),
            short_description="Hidden",
            price=50000,
            discount_percent=0,
            is_active=False,
        )

    def test_shop_view_shows_only_active_products(self):
        response = self.client.get(reverse("shop_view", args=[self.shop.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visible Product")
        self.assertNotContains(response, "Hidden Product")
