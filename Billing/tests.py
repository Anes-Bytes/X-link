from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from .models import UserPlan, Discount, Feature, Plan, Template
from core.test_utils import XLinkTestCase
from site_management.models import SiteContext, Customer

User = get_user_model()


class UserPlanModelTestCase(XLinkTestCase):
    """Test cases for UserPlan model"""

    def test_create_user_plan(self):
        """Test creating a user plan"""
        plan = UserPlan.objects.create(value="Basic")
        self.assertEqual(plan.value, "Basic")
        self.assertEqual(str(plan), "Basic")


class PlanModelTestCase(XLinkTestCase):
    """Test cases for Plan model"""

    def setUp(self):
        super().setUp()
        self.discount = Discount.objects.create(value=10)

    def test_create_plan(self):
        """Test creating a plan"""
        plan = Plan.objects.create(
            plan_type="Basic",
            name="Basic Plan",
            price=100000,
            discount=self.discount,
            is_special=False,
            period="monthly"
        )

        self.assertEqual(plan.plan_type, "Basic")
        self.assertEqual(plan.name, "Basic Plan")
        self.assertEqual(plan.price, 100000)
        self.assertEqual(plan.discount, self.discount)

    def test_get_discounted_price(self):
        """Test getting discounted price"""
        plan = Plan.objects.create(
            plan_type="Basic",
            name="Basic Plan",
            price=100000,
            discount=self.discount,
            is_special=False,
            period="monthly"
        )

        expected_price = 100000 * (1 - 10 / 100)  # 90000
        self.assertEqual(plan.get_discounted_price(), expected_price)


class BillingViewsTestCase(XLinkTestCase):
    """Test cases for billing views"""

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.discount = Discount.objects.create(value=10)

        # Create test plans
        self.monthly_plan = Plan.objects.create(
            plan_type="Basic",
            name="Basic Monthly",
            price=100000,
            discount=self.discount,
            is_special=False,
            period="monthly"
        )
        
        # Create site context and customer
        self.site_context = SiteContext.objects.create(
            site_name="Test Site",
            logo=self.test_image,
            hero_section_text_part1="Hero 1",
            hero_section_text_part2="Hero 2",
            hero_section_text_description="Hero Desc",
            footer_section_text_part1="Footer 1"
        )
        self.customer = Customer.objects.create(
            site_context=self.site_context,
            company_name="Test Company",
            company_url="https://test.com"
        )

    def test_landing_view(self):
        """Test landing view"""
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Billing/landing.html')
        self.assertIn('plans', response.context)
        self.assertIn('customers', response.context)
