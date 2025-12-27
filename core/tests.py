import json
from datetime import timedelta
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import CustomUser, OTP, UserMessages
from cards.models import UserCard
from Billing.models import UserPlan
from .test_utils import XLinkTestCase

User = get_user_model()


class CustomUserManagerTestCase(TestCase):
    """Test cases for CustomUser manager"""

    def test_create_user(self):
        """Test creating a user with required fields"""
        user = User.objects.create_user(
            phone="09123456789",
            full_name="Test User",
            password="testpass123"
        )
        self.assertEqual(user.phone, "09123456789")
        self.assertEqual(user.full_name, "Test User")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_phone(self):
        """Test creating user without phone raises ValueError"""
        with self.assertRaises(ValueError):
            User.objects.create_user(phone=None, full_name="Test User")

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.objects.create_superuser(
            phone="09123456789",
            full_name="Admin User",
            password="adminpass123"
        )
        self.assertEqual(user.phone, "09123456789")
        self.assertEqual(user.full_name, "Admin User")
        self.assertTrue(user.check_password("adminpass123"))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class CustomUserModelTestCase(TestCase):
    """Test cases for CustomUser model"""

    def setUp(self):
        self.user = User.objects.create_user(
            phone="09123456789",
            full_name="Test User"
        )

    def test_str_method(self):
        """Test string representation of user"""
        self.assertEqual(str(self.user), "Test User")

    def test_str_method_without_full_name(self):
        """Test string representation when full_name is None"""
        user = User(phone="09123456789")
        self.assertEqual(str(user), str(user.id))

    def test_plan_expires_none(self):
        """Test plan_expires when plan_expires_at is None"""
        self.assertIsNone(self.user.plan_expires())

    def test_plan_expires_future(self):
        """Test plan_expires with future expiration date"""
        future_date = timezone.now() + timedelta(days=30)
        self.user.plan_expires_at = future_date
        self.user.save()
        self.assertEqual(self.user.plan_expires(), 30)

    def test_plan_expires_past(self):
        """Test plan_expires with past expiration date"""
        past_date = timezone.now() - timedelta(days=5)
        self.user.plan_expires_at = past_date
        self.user.save()
        self.assertEqual(self.user.plan_expires(), 0)

    def test_is_expires_soon_none(self):
        """Test is_expires_soon when plan_expires_at is None"""
        self.assertFalse(self.user.is_expires_soon())

    def test_is_expires_soon_false(self):
        """Test is_expires_soon when expiration is far"""
        future_date = timezone.now() + timedelta(days=15)
        self.user.plan_expires_at = future_date
        self.user.save()
        self.assertFalse(self.user.is_expires_soon())

    def test_is_expires_soon_true(self):
        """Test is_expires_soon when expiration is soon"""
        soon_date = timezone.now() + timedelta(days=5)
        self.user.plan_expires_at = soon_date
        self.user.save()
        self.assertTrue(self.user.is_expires_soon())


class OTPModelTestCase(TestCase):
    """Test cases for OTP model"""

    def setUp(self):
        self.user = User.objects.create_user(
            phone="09123456789",
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
        self.assertEqual(str(otp), "09123456789 - 123456")

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


class UserMessagesModelTestCase(TestCase):
    """Test cases for UserMessages model"""

    def setUp(self):
        self.user = User.objects.create_user(
            phone="09123456789",
            full_name="Test User"
        )

    def test_create_message(self):
        """Test creating a user message"""
        message = UserMessages.objects.create(
            user=self.user,
            text="Test message",
            url="https://example.com"
        )
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.text, "Test message")
        self.assertEqual(message.url, "https://example.com")


class AuthenticationViewsTestCase(XLinkTestCase):
    """Test cases for authentication views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            phone="09123456789",
            full_name="Test User",
            password="testpass123"
        )

    def test_login_view_authenticated_user(self):
        """Test login view redirects authenticated users"""
        self.client.login(phone="09123456789", password="testpass123")
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'))

    def test_login_view_unauthenticated_user(self):
        """Test login view for unauthenticated users"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    def test_logout_view(self):
        """Test logout view"""
        self.client.login(phone="09123456789", password="testpass123")
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        # Check that user is logged out
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    @patch('core.views.send_sms')
    def test_request_otp_signup_valid(self, mock_send_sms):
        """Test requesting OTP for signup with valid data"""
        mock_send_sms.return_value = True

        response = self.client.post(reverse('request_otp'), {
            'phone': '09987654321',
            'full_name': 'New User'
        })

        self.assertRedirects(response, reverse('verify_otp'))
        self.assertTrue(User.objects.filter(phone='09987654321').exists())
        self.assertEqual(self.client.session['otp_phone'], '09987654321')
        self.assertTrue(self.client.session['is_signup'])

    @patch('core.views.send_sms')
    def test_request_otp_login_valid(self, mock_send_sms):
        """Test requesting OTP for login with valid data"""
        mock_send_sms.return_value = True

        response = self.client.post(reverse('request_otp'), {
            'phone': '09123456789'
        })

        self.assertRedirects(response, reverse('verify_otp'))
        self.assertEqual(self.client.session['otp_phone'], '09123456789')
        self.assertFalse(self.client.session['is_signup'])

    def test_request_otp_invalid_phone(self):
        """Test requesting OTP with invalid phone number"""
        response = self.client.post(reverse('request_otp'), {
            'phone': '123456789',  # Invalid format
            'full_name': 'Test User'
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('request_otp'), response['Location'])

    def test_request_otp_existing_user_signup(self):
        """Test requesting OTP for signup with existing phone"""
        response = self.client.post(reverse('request_otp'), {
            'phone': '09123456789',
            'full_name': 'Different Name'
        })

        self.assertRedirects(response, reverse('login'))

    def test_request_otp_nonexistent_user_login(self):
        """Test requesting OTP for login with non-existent phone"""
        response = self.client.post(reverse('request_otp'), {
            'phone': '09987654321'
        })

        self.assertRedirects(response, reverse('login'))

    def test_request_otp_rate_limit(self):
        """Test OTP request rate limiting"""
        # Set cache to simulate rate limit
        cache.set("otp_request_09123456789", True, timeout=60)

        response = self.client.post(reverse('request_otp'), {
            'phone': '09123456789'
        })

        self.assertRedirects(response, reverse('login'))

    def test_verify_otp_get_without_session(self):
        """Test verify OTP GET without session"""
        response = self.client.get(reverse('verify_otp'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('request_otp'), response['Location'])

    def test_verify_otp_get_with_session(self):
        """Test verify OTP GET with session"""
        # Ensure session is set properly
        session = self.client.session
        session['otp_phone'] = self.user.phone
        session.save()

        response = self.client.get(reverse('verify_otp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/verify.html')

    @patch('core.views.send_sms')
    def test_verify_otp_post_valid(self, mock_send_sms):
        """Test verifying OTP with valid code"""
        mock_send_sms.return_value = True

        # Create OTP
        otp = OTP.objects.create(
            user=self.user,
            code="123456",
            expires_at=timezone.now() + timedelta(minutes=2)
        )

        # Ensure session is set properly
        session = self.client.session
        session['otp_phone'] = self.user.phone
        session.save()

        response = self.client.post(reverse('verify_otp'), {
            'code': '123456'
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response['Location'])
        # Check user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)
        # Check OTP is deleted
        self.assertFalse(OTP.objects.filter(id=otp.id).exists())

    def test_verify_otp_post_invalid_code(self):
        """Test verifying OTP with invalid code"""
        self.client.session['otp_phone'] = '09123456789'
        self.client.session.save()

        # Ensure session is set properly
        session = self.client.session
        session['otp_phone'] = self.user.phone
        session.save()

        response = self.client.post(reverse('verify_otp'), {
            'code': '999999'
        })

        # Should redirect back to verify_otp for retry
        self.assertEqual(response.status_code, 302)
        self.assertIn('/verify-otp/', response['Location'])

    def test_verify_otp_post_expired_code(self):
        """Test verifying OTP with expired code"""
        # Create expired OTP
        OTP.objects.create(
            user=self.user,
            code="123456",
            expires_at=timezone.now() - timedelta(minutes=1)
        )

        # Ensure session is set properly
        session = self.client.session
        session['otp_phone'] = self.user.phone
        session.save()

        response = self.client.post(reverse('verify_otp'), {
            'code': '123456'
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('/verify-otp/', response['Location'])


class DashboardViewTestCase(XLinkTestCase):
    """Test cases for dashboard view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            phone="09123456789",
            full_name="Test User",
            password="testpass123"
        )
        self.basic_plan = UserPlan.objects.create(value="Basic")
        self.pro_plan = UserPlan.objects.create(value="Pro")

    def test_dashboard_view_unauthenticated(self):
        """Test dashboard view requires authentication"""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_view_authenticated_without_card(self):
        """Test dashboard view for authenticated user without card"""
        self.client.login(phone="09123456789", password="testpass123")
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/dashboard.html')
        self.assertIsNone(response.context['user_card'])
        self.assertIsNone(response.context['card_url'])

    def test_dashboard_view_authenticated_with_card(self):
        """Test dashboard view for authenticated user with card"""
        # Create user card
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        user_card = UserCard.objects.create(
            user=self.user,
            username="testuser",
            name="Test User",
            profile_picture=image
        )

        # Add user to a plan
        self.user.plan.add(self.basic_plan)

        self.client.login(phone="09123456789", password="testpass123")
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_card'], user_card)
        self.assertIn('testuser', response.context['card_url'])
        self.assertTrue(response.context['has_basic_plan'])
        self.assertFalse(response.context['has_pro_plan'])

