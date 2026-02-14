from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import SiteContext, Customer, Banners
from core.test_utils import XLinkTestCase

class SiteContextModelTestCase(XLinkTestCase):
    """Test cases for SiteContext model"""

    def setUp(self):
        super().setUp()
        self.logo = SimpleUploadedFile("logo.png", b"logo_content", content_type="image/png")

    def test_create_site_context(self):
        """Test creating a site context"""
        context = SiteContext.objects.create(
            site_name="X-Link",
            logo=self.logo,
            hero_section_text_part1="Create your",
            hero_section_text_part2="Digital Card",
            hero_section_text_description="Description",
            footer_section_text_part1="Footer Text"
        )
        self.assertEqual(context.site_name, "X-Link")
        self.assertEqual(str(context), "X-Link")


class CustomerModelTestCase(XLinkTestCase):
    """Test cases for Customer model"""

    def setUp(self):
        super().setUp()
        self.logo = SimpleUploadedFile("logo.png", b"logo_content", content_type="image/png")
        self.site_context = SiteContext.objects.create(
            site_name="X-Link",
            logo=self.logo,
            hero_section_text_part1="Part 1",
            hero_section_text_part2="Part 2",
            hero_section_text_description="Desc",
            footer_section_text_part1="Footer"
        )

    def test_create_customer(self):
        """Test creating a customer"""
        customer = Customer.objects.create(
            site_context=self.site_context,
            company_name="Test Company",
            company_url="https://test.com"
        )
        self.assertEqual(customer.company_name, "Test Company")
        self.assertEqual(str(customer), "Test Company")


class BannersModelTestCase(XLinkTestCase):
    """Test cases for Banners model"""

    def test_create_banner(self):
        """Test creating a banner"""
        banner = Banners.objects.create(
            title="Banner Title",
            description="Banner Description"
        )
        self.assertEqual(banner.title, "Banner Title")
        self.assertEqual(str(banner), "Banner Title")
