from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, phone, full_name=None, password=None):
        if not phone:
            raise ValueError('Phone is required')

        user = self.model(
            phone=phone,
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name="Admin", password=None):
        user = self.create_user(
            phone=phone,
            full_name=full_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def default_expire_time():
    return timezone.now() + timedelta(days=30)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserPlan(models.TextChoices):
        FREE = "free", "Free"
        BASIC = "basic", "Basic"
        PRO = "pro", "Pro"

    phone = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    EMAIL_FIELD = "email"             # ← بسیار مهم
    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = ["full_name"]

    plan = models.CharField(max_length=10, choices=UserPlan, default=UserPlan.FREE)
    plan_expires_at = models.DateTimeField(default=default_expire_time())

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def plan_expires(self):
        if not self.plan_expires_at:
            return 0
        delta = self.plan_expires_at.date() - timezone.now().date()
        return max(delta.days, 0)

    def __str__(self):
        return self.phone


class OTP(models.Model):
    user = models.ForeignKey("core.CustomUser", on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.phone} - {self.code}"


class Customers(models.Model):
    SiteContext = models.ForeignKey('SiteContext', on_delete=models.CASCADE, related_name='Customers')
    company_name = models.CharField(max_length=200)
    company_url = models.URLField()
    company_logo = models.ImageField(upload_to='company_logo')

    def __str__(self):
        return self.company_name


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
    class TypeChoices(models.TextChoices):
        Free = "Free", "Free"
        Basic = "Basic", "Basic"
        Pro = "Pro", "Pro"
    type = models.CharField(max_length=20, choices=TypeChoices.choices)
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
    footer_linkedin_url = models.URLField()
    footer_github_url = models.URLField()
    footer_instagram_url = models.URLField()

    def __str__(self):
        return self.site_name


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
        'core.Template',
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
        return f"{self.user.username} - {self.name}"

    def get_card_url(self):
        return f"https://x-link.ir/{self.username}"



    def clean(self):
        if self.user.plan == 'free' and self.color != 'default':
            raise ValidationError({
                'color': 'این رنگ فقط برای کاربران پلن پرمیوم و پایه فعال است. شما فقط میتوانید از رنگ پیشفرض ایکس لینک استفاده نمایید.'
            })


class Skill(models.Model):
    user_card = models.ForeignKey(UserCard, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user_card.name} - {self.name}"


class Banners(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners', blank=True)

    def __str__(self):
        return self.title


class Template(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='templates')
    delay = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name