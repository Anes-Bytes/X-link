from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class Customers(models.Model):
    SiteContext = models.ForeignKey('SiteContext', on_delete=models.CASCADE, related_name='Customers')
    company_name = models.CharField(max_length=200)
    company_url = models.URLField()
    company_logo = models.ImageField(upload_to='company_logo')

    def __str__(self):
        return self.company_name


class Templates(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='templates')
    delay = models.IntegerField()

    def __str__(self):
        return self.name


class Feature(models.Model):
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, related_name='Features')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Discount(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return f"{self.value}%"


class Plan(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='+')
    is_special = models.BooleanField()

    def get_final_price(self):
        if not self.discount:
            return self.price
        return max(self.price * (1 - self.discount.value / 100), 0)

    def __str__(self):
        return self.name


class SiteContext(models.Model):
    site_name = models.CharField(max_length=100)
    hero_section_text_part1 = models.CharField(max_length=200)
    hero_section_text_part2 = models.CharField(max_length=200)
    hero_section_text_description = models.CharField(max_length=200)

    footer_section_text_part1 = models.CharField(max_length=200)
    footer_telegram_url = models.URLField()
    footer_linkdin_url = models.URLField()
    footer_github_url = models.URLField()
    footer_instagram_url = models.URLField()

    def __str__(self):
        return self.site_name


class UserCard(models.Model):
    COLOR_CHOICES = (
        ('default', 'Default X-Link'),
        ('blue', 'Blue'),
        ('gold', 'Gold'),
        ('orange', 'Orange'),
        ('gray', 'Gray'),
        ('mint', 'Mint'),
        ('pink', 'Pink'),
        ('purple', 'Purple'),
        ('red', 'Red'),
        ('green', 'Green'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_card')
    username = models.SlugField(max_length=255, unique=True)
    template = models.ForeignKey(
        'Xlink.CardTemplate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_cards'
    )
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='default')
    
    # User Info Fields
    name = models.CharField(max_length=255)
    short_bio = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    
    # Social Media
    instagram_username = models.CharField(max_length=255, blank=True)
    telegram_username = models.CharField(max_length=255, blank=True)
    linkedin_username = models.CharField(max_length=255, blank=True)
    youtube_username = models.CharField(max_length=255, blank=True)
    twitter_username = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    def get_card_url(self):
        return f"https://example.com/{self.username}"


class Skill(models.Model):
    user_card = models.ForeignKey(UserCard, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user_card.name} - {self.name}"
