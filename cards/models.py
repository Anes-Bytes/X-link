from django.core.exceptions import ValidationError
from django.db import models

from Billing.models import Template
from core.models import CustomUser


class UserCard(models.Model):
    """
    Digital business card for users.
    """

    # Color Themes
    COLOR_CHOICES = (
        ('default', 'ایکس‌لینک پیش‌فرض'),
        ('gold', 'طلایی'),
        ('orange', 'نارنجی'),
        ('gray', 'خاکستری'),
        ('mint', 'نعنایی'),
        ('pink', 'صورتی'),
        ('purple', 'بنفش'),
        ('red', 'قرمز'),
        ('green', 'سبز'),
    )

    # Relationships
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user_card',
        help_text="User who owns this card"
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_cards',
        help_text="Card template/styling"
    )

    # Basic Information
    name = models.CharField(
        max_length=255,
        help_text="Full name displayed on card"
    )
    username = models.SlugField(
        max_length=32,
        unique=True,
        help_text="Unique URL slug for the card"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics',
        help_text="Profile picture for the card"
    )

    # Contact Information
    phone_number = models.CharField(
        max_length=255,
        blank=True,
        help_text="Phone number to display"
    )
    email = models.EmailField(
        blank=True,
        help_text="Email address to display"
    )
    website = models.URLField(
        blank=True,
        help_text="Personal website URL"
    )

    # Content
    short_bio = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short biography/tagline"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description/about section"
    )

    # Social Media Profiles
    instagram_username = models.CharField(
        max_length=255,
        blank=True,
        help_text="Instagram username"
    )
    telegram_username = models.CharField(
        max_length=255,
        blank=True,
        help_text="Telegram username"
    )
    linkedin_username = models.CharField(
        max_length=255,
        blank=True,
        help_text="LinkedIn username"
    )
    youtube_username = models.CharField(
        max_length=255,
        blank=True,
        help_text="YouTube channel username"
    )
    twitter_username = models.CharField(
        max_length=255,
        blank=True,
        help_text="Twitter/X username"
    )
    github_username = models.CharField(
        max_length=255,
        blank=True,
        help_text="GitHub username"
    )

    # Appearance & Features
    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default='default',
        help_text="Card color theme"
    )
    blue_tick = models.BooleanField(
        default=False,
        help_text="Show blue verification tick"
    )
    stars_background = models.BooleanField(
        default=False,
        help_text="Show animated stars background"
    )
    black_background = models.BooleanField(
        default=False,
        help_text="Use black background theme"
    )

    # Analytics & Settings
    views = models.PositiveIntegerField(
        default=0,
        help_text="Number of times card was viewed"
    )
    show_views = models.BooleanField(
        default=False,
        help_text="Whether to display view count on card"
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Whether card is publicly accessible"
    )

    # Audit Fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this card was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this card was last updated"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['is_published', 'username']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        """
        String representation of the user card.
        """
        return f"{self.name} (@{self.username})"

    def get_card_url(self, request=None):
        """
        Get the full URL for this card.

        Args:
            request: Django request object to build absolute URL

        Returns:
            str: Full URL to the card
        """
        if request:
            scheme = request.scheme
            host = request.get_host()
            return f"{scheme}://{host}/{self.username}/"

        # Fallback - should be configurable
        return f"https://x-link.ir/{self.username}/"

    def increment_views(self):
        """
        Increment the view count for this card.
        """
        self.views = models.F('views') + 1
        self.save(update_fields=['views'])

    def has_social_links(self):
        """
        Check if user has any social media links configured.

        Returns:
            bool: True if at least one social link is set
        """
        social_fields = [
            'instagram_username', 'telegram_username', 'linkedin_username',
            'youtube_username', 'twitter_username', 'github_username'
        ]
        return any(getattr(self, field) for field in social_fields)

    def get_social_links(self):
        """
        Get dictionary of configured social media links.

        Returns:
            dict: Dictionary with platform names as keys and usernames as values
        """
        links = {}
        if self.instagram_username:
            links['instagram'] = self.instagram_username
        if self.telegram_username:
            links['telegram'] = self.telegram_username
        if self.linkedin_username:
            links['linkedin'] = self.linkedin_username
        if self.youtube_username:
            links['youtube'] = self.youtube_username
        if self.twitter_username:
            links['twitter'] = self.twitter_username
        if self.github_username:
            links['github'] = self.github_username
        return links

    def can_use_color(self, color):
        if not self.user_id:
            return color == 'default'

        if color == 'default':
            return True

        return self.user.has_plan('Basic') or self.user.has_plan('Pro')

    def clean(self):
        super().clean()

        # اگر یوزر هنوز ست نشده
        if not self.user_id:
            if self.color != 'default':
                raise ValidationError({
                    'color': 'در حال حاضر فقط رنگ پیش‌فرض قابل انتخاب است.'
                })
            return

        # Validate color permissions (وقتی user داریم)
        if not self.can_use_color(self.color):
            raise ValidationError({
                'color': 'این رنگ فقط برای کاربران با پلن پایه یا حرفه‌ای فعال است. لطفاً پلن خود را ارتقا دهید.'
            })

        # Validate username format
        if self.username and not self.username.replace('-', '').replace('_', '').isalnum():
            raise ValidationError({
                'username': 'نام کاربری فقط می‌تواند شامل حروف، اعداد، خط تیره و زیرخط باشد.'
            })


class Skill(models.Model):
    user_card = models.ForeignKey(UserCard, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user_card.name} - {self.name}"


class Service(models.Model):
    user_card = models.ForeignKey(UserCard, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user_card.name} - {self.title}"


class Portfolio(models.Model):
    user_card = models.ForeignKey(UserCard, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='portfolio')
    url = models.URLField(blank=True, help_text="Project URL or external link")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Portfolio Items"

    def __str__(self):
        return f"{self.user_card.name} - {self.title}"

