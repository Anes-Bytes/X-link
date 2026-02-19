"""
Test utilities and helper functions for Django testing.
"""
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from cards.models import UserCard
from Billing.models import UserPlan, Template, Discount, Plan

User = get_user_model()


@override_settings(SECURE_SSL_REDIRECT=False)
class XLinkTestCase(TestCase):
    """
    Base test case class with common test utilities for X-Link project.
    """

    def setUp(self):
        """Set up common test data"""
        super().setUp()
        self.test_image = SimpleUploadedFile(
            "test.jpg",
            b"test_image_content",
            content_type="image/jpeg"
        )
        # Ensure Free plan exists for signals
        UserPlan.objects.get_or_create(value="Free")

    def create_test_user(self, username="testuser", full_name="Test User", password="testpass123", **kwargs):
        """Create a test user with default values"""
        return User.objects.create_user(
            username=username,
            full_name=full_name,
            password=password,
            **kwargs
        )

    def create_test_user_card(self, user=None, username="testuser", name="Test User", **kwargs):
        """Create a test user card with default values"""
        if user is None:
            user = self.create_test_user()

        defaults = {
            'user': user,
            'username': username,
            'name': name,
            'profile_picture': self.test_image,
            'is_published': True,
        }
        defaults.update(kwargs)

        return UserCard.objects.create(**defaults)

    def create_test_plan(self, plan_type="Basic", name="Basic Plan", price=100000, period="monthly", **kwargs):
        """Create a test plan with default values"""
        discount = kwargs.pop('discount', None)
        if discount is None:
            discount = Discount.objects.create(value=0)

        defaults = {
            'plan_type': plan_type,
            'name': name,
            'price': price,
            'discount': discount,
            'is_special': False,
            'period': period,
        }
        defaults.update(kwargs)

        return Plan.objects.create(**defaults)

    def create_test_template(self, name="Test Template", **kwargs):
        """Create a test template with default values"""
        defaults = {
            'name': name,
            'image': self.test_image,
            'delay': 5,
            'is_active': True,
        }
        defaults.update(kwargs)

        return Template.objects.create(**defaults)

    def create_test_user_plan(self, value="Basic"):
        """Create a test user plan"""
        return UserPlan.objects.create(value=value)

    def login_user(self, user=None):
        """Login a user for testing authenticated views"""
        if user is None:
            user = self.create_test_user()
        self.client.login(username=user.username, password="testpass123")
        return user

    def assert_response_unauthenticated(self, url, method='get', data=None):
        """Assert that a URL requires authentication"""
        if method.lower() == 'get':
            response = self.client.get(url)
        elif method.lower() == 'post':
            response = self.client.post(url, data=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login', response['Location'])


def create_authenticated_client(user=None):
    """
    Create a test client with an authenticated user.
    Useful for testing views that require authentication.
    """
    from django.test import Client

    if user is None:
        # Create a test user
        user = User.objects.create_user(
            username="testuser",
            full_name="Test User",
            password="testpass123"
        )

    client = Client()
    client.login(username=user.username, password="testpass123")
    return client, user


def create_user_with_card(plan_type=None):
    """
    Create a user with a card and optionally assign a plan.
    Returns (user, user_card)
    """
    user = User.objects.create_user(
        username="testuser",
        full_name="Test User",
        password="testpass123"
    )

    image = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")
    user_card = UserCard.objects.create(
        user=user,
        username="testuser",
        name="Test User",
        profile_picture=image
    )

    if plan_type:
        plan = UserPlan.objects.create(value=plan_type)
        user.plan.add(plan)

    return user, user_card


def create_complete_user_card(user):
    """
    Create a complete user card with skills, services, and portfolio items.
    """
    image = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")
    user_card = UserCard.objects.create(
        user=user,
        username="testuser",
        name="Test User",
        short_bio="Software Developer",
        phone_number="09123456789",
        description="Experienced developer",
        email="test@example.com",
        website="https://example.com",
        instagram_username="@testuser",
        profile_picture=image
    )

    # Add skills
    from cards.models import Skill, Service, Portfolio
    Skill.objects.create(user_card=user_card, name="Python")
    Skill.objects.create(user_card=user_card, name="Django")

    # Add services
    Service.objects.create(
        user_card=user_card,
        title="Web Development",
        description="Full stack web development services"
    )

    # Add portfolio
    portfolio_image = SimpleUploadedFile("portfolio.jpg", b"portfolio_content", content_type="image/jpeg")
    Portfolio.objects.create(
        user_card=user_card,
        title="E-commerce Site",
        description="Built with Django and React",
        image=portfolio_image,
        url="https://example.com/project"
    )

    return user_card
