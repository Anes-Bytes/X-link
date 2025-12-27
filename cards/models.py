from django.core.exceptions import ValidationError
from django.db import models

from Billing.models import Template
from core.models import CustomUser


class UserCard(models.Model):
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

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_card')
    blue_tick = models.BooleanField(default=False)
    stars_background = models.BooleanField(default=False)
    black_background = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    show_views = models.BooleanField(default=False)
    username = models.SlugField(max_length=32, unique=True, validators=[])
    profile_picture = models.ImageField(upload_to='profile_pics')
    template = models.ForeignKey(
        Template,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_cards'
    )
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='default')

    # User Info Fields
    name = models.CharField(max_length=255)
    short_bio = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    # Social Media
    instagram_username = models.CharField(max_length=255, blank=True)
    telegram_username = models.CharField(max_length=255, blank=True)
    linkedin_username = models.CharField(max_length=255, blank=True)
    youtube_username = models.CharField(max_length=255, blank=True)
    twitter_username = models.CharField(max_length=255, blank=True)
    github_username = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.phone} - {self.name}"

    def get_card_url(self):
        return f"https://x-link.ir/{self.username}"

    def clean(self):
        super().clean()

        if not self.user_id:
            if self.color != 'default':
                raise ValidationError({
                    'color': 'این رنگ فقط برای کاربران پلن پایه و پرمیوم فعال است. شما فقط می‌توانید از رنگ پیش‌فرض استفاده کنید.'
                })
            return

        user_plans = set(self.user.plan.values_list('value', flat=True))
        allowed_colors = {'Basic', 'Pro'}

        if self.color != 'default' and user_plans.isdisjoint(allowed_colors):
            raise ValidationError({
                'color': 'این رنگ فقط برای کاربران پلن پایه و پرمیوم فعال است. شما فقط می‌توانید از رنگ پیش‌فرض استفاده کنید.'
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

