from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import UserPlan, Discount, Feature, Plan, Template
from core.test_utils import XLinkTestCase


class UserPlanModelTestCase(TestCase):
    """Test cases for UserPlan model"""

    def test_create_user_plan(self):
        """Test creating a user plan"""
        plan = UserPlan.objects.create(value="Basic")
        self.assertEqual(plan.value, "Basic")
        self.assertEqual(str(plan), "Basic")


class DiscountModelTestCase(TestCase):
    """Test cases for Discount model"""

    def test_create_discount(self):
        """Test creating a discount"""
        discount = Discount.objects.create(value=20)
        self.assertEqual(discount.value, 20)
        self.assertEqual(str(discount), "20%")


class FeatureModelTestCase(TestCase):
    """Test cases for Feature model"""

    def test_create_feature(self):
        """Test creating a feature"""
        plan = Plan.objects.create(
            type="Basic",
            name="Basic Plan",
            price=100000,
            discount=Discount.objects.create(value=10),
            is_special=False,
            period="monthly"
        )
        feature = Feature.objects.create(plan=plan, name="Feature 1")
        self.assertEqual(feature.plan, plan)
        self.assertEqual(feature.name, "Feature 1")
        self.assertEqual(str(feature), "Feature 1")


class PlanModelTestCase(TestCase):
    """Test cases for Plan model"""

    def setUp(self):
        self.discount = Discount.objects.create(value=10)

    def test_create_plan(self):
        """Test creating a plan"""
        plan = Plan.objects.create(
            type="Basic",
            name="Basic Plan",
            price=100000,
            discount=self.discount,
            is_special=False,
            period="monthly"
        )

        self.assertEqual(plan.type, "Basic")
        self.assertEqual(plan.name, "Basic Plan")
        self.assertEqual(plan.price, 100000)
        self.assertEqual(plan.discount, self.discount)
        self.assertFalse(plan.is_special)
        self.assertEqual(plan.period, "monthly")
        self.assertEqual(str(plan), "Basic Plan")

    def test_get_final_price_with_discount(self):
        """Test getting final price with discount"""
        plan = Plan.objects.create(
            type="Basic",
            name="Basic Plan",
            price=100000,
            discount=self.discount,
            is_special=False,
            period="monthly"
        )

        expected_final_price = 100000 * (1 - 10 / 100)  # 90000
        self.assertEqual(plan.get_final_price(), expected_final_price)

    def test_get_final_price_without_discount(self):
        """Test getting final price without discount"""
        zero_discount = Discount.objects.create(value=0)
        plan = Plan.objects.create(
            type="Pro",
            name="Pro Plan",
            price=200000,
            discount=zero_discount,
            is_special=False,
            period="monthly"
        )

        self.assertEqual(plan.get_final_price(), 200000)

    def test_get_final_price_zero_discount(self):
        """Test getting final price with zero discount"""
        zero_discount = Discount.objects.create(value=0)
        plan = Plan.objects.create(
            type="Free",
            name="Free Plan",
            price=0,
            discount=zero_discount,
            is_special=False,
            period="monthly"
        )

        self.assertEqual(plan.get_final_price(), 0)


class TemplateModelTestCase(TestCase):
    """Test cases for Template model"""

    def setUp(self):
        self.image = SimpleUploadedFile("template.jpg", b"template_content", content_type="image/jpeg")

    def test_create_template(self):
        """Test creating a template"""
        template = Template.objects.create(
            name="Test Template",
            image=self.image,
            description="Test description",
            delay=5,
            only_for_premium=False,
            is_active=True
        )

        self.assertEqual(template.name, "Test Template")
        self.assertEqual(template.description, "Test description")
        self.assertEqual(template.delay, 5)
        self.assertFalse(template.only_for_premium)
        self.assertTrue(template.is_active)
        self.assertEqual(str(template), "Test Template")


class BillingViewsTestCase(XLinkTestCase):
    """Test cases for billing views"""

    def setUp(self):
        self.client = Client()
        self.discount = Discount.objects.create(value=10)

        # Create test plans
        self.monthly_plan = Plan.objects.create(
            type="Basic",
            name="Basic Monthly",
            price=100000,
            discount=self.discount,
            is_special=False,
            period="monthly"
        )
        self.annual_plan = Plan.objects.create(
            type="Pro",
            name="Pro Annual",
            price=1000000,
            discount=self.discount,
            is_special=False,
            period="annual"
        )

        # Create test templates
        self.template_image = SimpleUploadedFile("template.jpg", b"content", content_type="image/jpeg")
        self.template = Template.objects.create(
            name="Test Template",
            image=self.template_image,
            delay=5,
            is_active=True
        )

        # Create test customers (from site_management)
        from site_management.models import SiteContext, Customer
        self.site_context = SiteContext.objects.create(
            site_name="Test Site",
            logo=self.template_image,
            hero_section_text_part1="Hero Text",
            hero_section_text_part2="Hero Text 2",
            hero_section_text_description="Description"
        )
        self.customer = Customer.objects.create(
            SiteContext=self.site_context,
            company_name="Test Company",
            company_url="https://test.com",
            company_logo=self.template_image
        )

    def test_landing_view_monthly(self):
        """Test landing view with monthly period"""
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Billing/landing.html')
        self.assertIn('templates', response.context)
        self.assertIn('customers', response.context)
        self.assertIn('Billing', response.context)
        self.assertEqual(response.context['current_period'], 'monthly')

    def test_landing_view_annual(self):
        """Test landing view with annual period"""
        response = self.client.get(reverse('home') + '?period=annual')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_period'], 'annual')

    def test_landing_view_invalid_period(self):
        """Test landing view with invalid period defaults to monthly"""
        response = self.client.get(reverse('home') + '?period=invalid')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_period'], 'monthly')

    def test_landing_view_caching(self):
        """Test that landing view uses caching"""
        # Clear cache first
        cache.clear()

        # First request should cache data
        response1 = self.client.get(reverse('home'))
        self.assertEqual(response1.status_code, 200)

        # Check that cache keys exist
        self.assertIsNotNone(cache.get('landing_plans_monthly'))
        self.assertIsNotNone(cache.get('landing_templates'))
        self.assertIsNotNone(cache.get('landing_customers'))

        # Second request should use cached data
        response2 = self.client.get(reverse('home'))
        self.assertEqual(response2.status_code, 200)

    def test_pricing_view_monthly(self):
        """Test pricing view with monthly period"""
        response = self.client.get(reverse('pricing') + '?period=monthly')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/pricing.html')
        self.assertIn('Billing', response.context)
        self.assertEqual(response.context['current_period'], 'monthly')

    def test_pricing_view_annual(self):
        """Test pricing view with annual period"""
        response = self.client.get(reverse('pricing') + '?period=annual')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_period'], 'annual')

    def test_pricing_view_default(self):
        """Test pricing view with default period"""
        response = self.client.get(reverse('pricing'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_period'], None)

    def test_payment_success_view_unauthenticated(self):
        """Test payment success view requires authentication"""
        response = self.client.get(reverse('payment_success'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('payment_success')}")

    def test_payment_success_view_authenticated(self):
        """Test payment success view for authenticated user"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(
            phone="09123456789",
            full_name="Test User",
            password="testpass123"
        )

        self.client.login(phone="09123456789", password="testpass123")
        response = self.client.get(reverse('payment_success'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/payment-success.html')

    def test_payment_failed_view_unauthenticated(self):
        """Test payment failed view requires authentication"""
        response = self.client.get(reverse('payment_failed'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('payment_failed')}")

    def test_payment_failed_view_authenticated(self):
        """Test payment failed view for authenticated user"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(
            phone="09123456789",
            full_name="Test User",
            password="testpass123"
        )

        self.client.login(phone="09123456789", password="testpass123")
        response = self.client.get(reverse('payment_failed'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/payment-failed.html')

    def test_about_view(self):
        """Test about view"""
        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Billing/about.html')
