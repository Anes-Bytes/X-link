import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from .models import UserCard, Skill, Service, Portfolio
from Billing.models import UserPlan, Template
from core.forms import UserCardForm, SkillInlineFormSet, ServiceInlineFormSet, PortfolioInlineFormSet
from core.test_utils import XLinkTestCase

User = get_user_model()


class UserCardModelTestCase(XLinkTestCase):
    """Test cases for UserCard model"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser",
            full_name="Test User"
        )
        self.basic_plan = UserPlan.objects.create(value="Basic")
        self.pro_plan = UserPlan.objects.create(value="Pro")
        self.template = Template.objects.create(
            name="Test Template",
            delay=5
        )
        self.image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    def test_create_user_card(self):
        """Test creating a user card"""
        user_card = UserCard.objects.create(
            user=self.user,
            username="testuser",
            name="Test User",
            profile_picture=self.image
        )

        self.assertEqual(user_card.user, self.user)
        self.assertEqual(user_card.username, "testuser")
        self.assertEqual(user_card.name, "Test User")
        self.assertEqual(user_card.views, 0)
        self.assertTrue(user_card.is_published)

    def test_get_card_url(self):
        """Test getting card URL"""
        user_card = UserCard.objects.create(
            user=self.user,
            username="testuser",
            name="Test User",
            profile_picture=self.image
        )

        # Base URL might depend on request, but model method might have hardcoded domain or use settings
        url = user_card.get_card_url()
        self.assertIn("testuser", url)

    def test_clean_valid_default_color(self):
        """Test clean method with valid default color"""
        user_card = UserCard(
            user=self.user,
            username="testuser",
            name="Test User",
            color="default",
            profile_picture=self.image
        )
        user_card.full_clean()  # Should not raise exception

    def test_clean_invalid_color_without_plan(self):
        """Test clean method with invalid color for user without plan"""
        user_card = UserCard(
            user=self.user,
            username="testuser",
            name="Test User",
            color="gold",
            profile_picture=self.image
        )

        with self.assertRaises(ValidationError):
            user_card.full_clean()


class SkillModelTestCase(XLinkTestCase):
    """Test cases for Skill model"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser",
            full_name="Test User"
        )
        self.image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        self.user_card = UserCard.objects.create(
            user=self.user,
            username="testuser",
            name="Test User",
            profile_picture=self.image
        )

    def test_create_skill(self):
        """Test creating a skill"""
        skill = Skill.objects.create(
            user_card=self.user_card,
            name="Python"
        )

        self.assertEqual(skill.user_card, self.user_card)
        self.assertEqual(skill.name, "Python")


class CardViewsTestCase(XLinkTestCase):
    """Test cases for card-related views"""

    def setUp(self):
        super().setUp()
        self.user = self.create_test_user()
        self.basic_plan = self.create_test_user_plan("Basic")
        self.pro_plan = self.create_test_user_plan("Pro")
        self.template = self.create_test_template()

    def test_card_builder_view_unauthenticated(self):
        """Test card builder view requires authentication"""
        response = self.client.get(reverse('card_builder'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('card_builder')}")

    def test_card_builder_view_authenticated_get(self):
        """Test card builder view GET request"""
        self.login_user(self.user)
        response = self.client.get(reverse('card_builder'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_builder.html')

    def test_view_card_published(self):
        """Test viewing a published card"""
        user_card = UserCard.objects.create(
            user=self.user,
            username="testusercard",
            name="Test User",
            profile_picture=self.test_image,
            is_published=True,
            views=0
        )

        response = self.client.get(reverse('view_card', kwargs={'username': 'testusercard'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_view.html')
        self.assertEqual(response.context['user_card'], user_card)
        
        # Check views incremented
        user_card.refresh_from_db()
        self.assertEqual(user_card.views, 1)

    def test_view_card_unpublished(self):
        """Test viewing an unpublished card"""
        UserCard.objects.create(
            user=self.user,
            username="unpublished",
            name="Test User",
            profile_picture=self.test_image,
            is_published=False
        )

        response = self.client.get(reverse('view_card', kwargs={'username': 'unpublished'}))
        self.assertEqual(response.status_code, 404)
