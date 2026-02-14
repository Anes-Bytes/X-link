from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import CustomUser, OTP
from cards.models import UserCard
from Billing.models import UserPlan
from .test_utils import XLinkTestCase

User = get_user_model()


class CustomUserManagerTestCase(XLinkTestCase):
    """Test cases for CustomUser manager"""

    def test_create_user(self):
        """Test creating a user with required fields"""
        user = User.objects.create_user(
            username="testuser",
            full_name="Test User",
            password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.full_name, "Test User")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_username(self):
        """Test creating user without username raises ValueError"""
        with self.assertRaises(ValueError):
            User.objects.create_user(username=None, full_name="Test User")

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.objects.create_superuser(
            username="adminuser",
            full_name="Admin User",
            password="adminpass123"
        )
        self.assertEqual(user.username, "adminuser")
        self.assertEqual(user.full_name, "Admin User")
        self.assertTrue(user.check_password("adminpass123"))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class CustomUserModelTestCase(XLinkTestCase):
    """Test cases for CustomUser model"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser",
            full_name="Test User"
        )

    def test_str_method(self):
        """Test string representation of user"""
        self.assertEqual(str(self.user), "Test User (testuser)")

    def test_get_remaining_days_none(self):
        """Test get_remaining_days when plan_expires_at is None"""
        self.assertIsNone(self.user.get_remaining_days())

    def test_get_remaining_days_future(self):
        """Test get_remaining_days with future expiration date"""
        future_date = timezone.now() + timedelta(days=30)
        self.user.plan_expires_at = future_date
        self.user.save()
        self.assertEqual(self.user.get_remaining_days(), 30)

    def test_is_plan_expiring_soon_none(self):
        """Test is_plan_expiring_soon when plan_expires_at is None"""
        self.assertFalse(self.user.is_plan_expiring_soon())

    def test_is_plan_expiring_soon_true(self):
        """Test is_plan_expiring_soon when expiration is soon"""
        soon_date = timezone.now() + timedelta(days=5)
        self.user.plan_expires_at = soon_date
        self.user.save()
        self.assertTrue(self.user.is_plan_expiring_soon())


class OTPModelTestCase(XLinkTestCase):
    """Test cases for OTP model"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser",
            full_name="Test User"
        )

    def test_create_otp(self):
        """Test creating OTP"""
        expires_at = timezone.now() + timedelta(minutes=2)
        otp = OTP.objects.create(
            user=self.user,
            code="123456",
            expires_at=expires_at
        )
        self.assertEqual(otp.user, self.user)
        self.assertEqual(otp.code, "123456")

    def test_is_expired_false(self):
        """Test is_expired when OTP is still valid"""
        future_time = timezone.now() + timedelta(minutes=1)
        otp = OTP.objects.create(
            user=self.user,
            code="123456",
            expires_at=future_time
        )
        self.assertFalse(otp.is_expired())

    def test_is_expired_true(self):
        """Test is_expired when OTP has expired"""
        past_time = timezone.now() - timedelta(minutes=1)
        otp = OTP.objects.create(
            user=self.user,
            code="123456",
            expires_at=past_time
        )
        self.assertTrue(otp.is_expired())


class AuthenticationViewsTestCase(XLinkTestCase):
    """Test cases for authentication views"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser",
            full_name="Test User",
            password="testpass123"
        )

    def test_login_view_authenticated_user(self):
        """Test login view redirects authenticated users"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_view_unauthenticated_user(self):
        """Test login view for unauthenticated users"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    def test_signup_view_authenticated_user(self):
        """Test signup view redirects authenticated users"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('signup'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_logout_view(self):
        """Test logout view"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        
    def test_dashboard_view_unauthenticated(self):
        """Test dashboard view requires authentication"""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_view_authenticated(self):
        """Test dashboard view for authenticated user"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/dashboard.html')
