from django.db import models

class SiteContext(models.Model):
    """
    Site-wide configuration and content.
    """

    # Basic Site Information
    site_name = models.CharField(
        max_length=100,
        help_text="Name of the website"
    )
    logo = models.ImageField(
        upload_to='logo',
        help_text="Site logo image"
    )

    # Hero Section Content
    hero_section_text_part1 = models.CharField(
        max_length=200,
        help_text="First part of hero section text"
    )
    hero_section_text_part2 = models.CharField(
        max_length=200,
        help_text="Second part of hero section text"
    )
    hero_section_text_description = models.CharField(
        max_length=500,
        help_text="Hero section description text"
    )

    # Footer Content
    footer_section_text_part1 = models.CharField(
        max_length=200,
        help_text="Footer section text"
    )

    # Social Media Links
    footer_telegram_url = models.URLField(
        null=True,
        blank=True,
        help_text="Telegram profile URL"
    )
    footer_linkedin_url = models.URLField(
        null=True,
        blank=True,
        help_text="LinkedIn profile URL"
    )
    footer_github_url = models.URLField(
        null=True,
        blank=True,
        help_text="GitHub profile URL"
    )
    footer_instagram_url = models.URLField(
        null=True,
        blank=True,
        help_text="Instagram profile URL"
    )

    # Audit Fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this site context was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this site context was last updated"
    )

    class Meta:
        verbose_name = "Site Context"
        verbose_name_plural = "Site Contexts"

    def get_social_links(self):
        """
        Get dictionary of active social media links.

        Returns:
            dict: Dictionary with social platform names as keys and URLs as values
        """
        links = {}
        if self.footer_telegram_url:
            links['telegram'] = self.footer_telegram_url
        if self.footer_linkedin_url:
            links['linkedin'] = self.footer_linkedin_url
        if self.footer_github_url:
            links['github'] = self.footer_github_url
        if self.footer_instagram_url:
            links['instagram'] = self.footer_instagram_url
        return links

    def __str__(self):
        return self.site_name


class Banners(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.title


class Customer(models.Model):
    """
    Customer/company testimonial or logo display.
    """

    site_context = models.ForeignKey(
        'SiteContext',
        on_delete=models.CASCADE,
        related_name='customers',
        help_text="Site context this customer belongs to"
    )
    company_name = models.CharField(
        max_length=200,
        help_text="Name of the company/customer"
    )
    company_url = models.URLField(
        help_text="Company website URL"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether to display this customer"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this customer was added"
    )

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['display_order', 'company_name']

    def __str__(self):
        return self.company_name
