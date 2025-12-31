from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import SiteContext, Banners, Customer


class SiteContextModelTestCase(TestCase):
    """Test cases for SiteContext model"""

    def setUp(self):
        self.logo = SimpleUploadedFile("logo.png", b"logo_content", content_type="image/png")

    def test_create_site_context(self):
        """Test creating a site context"""
        site_context = SiteContext.objects.create(
            site_name="X-Link",
            logo=self.logo,
            hero_section_text_part1="Welcome to",
            hero_section_text_part2="X-Link",
            hero_section_text_description="Create your digital business card",
            footer_section_text_part1="Follow us on social media",
            footer_telegram_url="https://t.me/xlink",
            footer_linkedin_url="https://linkedin.com/company/xlink",
            footer_github_url="https://github.com/xlink",
            footer_instagram_url="https://instagram.com/xlink"
        )

        self.assertEqual(site_context.site_name, "X-Link")
        self.assertEqual(site_context.hero_section_text_part1, "Welcome to")
        self.assertEqual(site_context.hero_section_text_part2, "X-Link")
        self.assertEqual(site_context.footer_telegram_url, "https://t.me/xlink")
        self.assertEqual(str(site_context), "X-Link")


class BannersModelTestCase(TestCase):
    """Test cases for Banners model"""

    def setUp(self):
        self.banner_image = SimpleUploadedFile("banner.jpg", b"banner_content", content_type="image/jpeg")

    def test_create_banner(self):
        """Test creating a banner"""
        banner = Banners.objects.create(
            title="Welcome Banner",
            description="Welcome to our platform",
            image=self.banner_image
        )

        self.assertEqual(banner.title, "Welcome Banner")
        self.assertEqual(banner.description, "Welcome to our platform")
        self.assertEqual(str(banner), "Welcome Banner")

    def test_create_banner_without_image(self):
        """Test creating a banner without image"""
        banner = Banners.objects.create(
            title="Text Banner",
            description="Banner with text only"
        )

        self.assertEqual(banner.title, "Text Banner")
        self.assertEqual(banner.image.name, "")  # Django ImageField returns empty string when no image


class CustomerModelTestCase(TestCase):
    """Test cases for Customer model"""

    def setUp(self):
        self.logo = SimpleUploadedFile("logo.png", b"logo_content", content_type="image/png")
        self.site_context = SiteContext.objects.create(
            site_name="X-Link",
            logo=self.logo,
            hero_section_text_part1="Welcome",
            hero_section_text_part2="to X-Link",
            hero_section_text_description="Digital business cards"
        )
        self.company_logo = SimpleUploadedFile("company.png", b"company_content", content_type="image/png")

    def test_create_customer(self):
        """Test creating a customer"""
        customer = Customer.objects.create(
            SiteContext=self.site_context,
            company_name="Tech Corp",
            company_url="https://techcorp.com",
            company_logo=self.company_logo
        )

        self.assertEqual(customer.SiteContext, self.site_context)
        self.assertEqual(customer.company_name, "Tech Corp")
        self.assertEqual(customer.company_url, "https://techcorp.com")
        self.assertEqual(str(customer), "Tech Corp")
