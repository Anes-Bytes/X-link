from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from datetime import timedelta

from Billing.models import UserPlan

class UserManager(BaseUserManager):
    """
    Custom manager for CustomUser model with phone-based authentication.
    """

    def create_user(self, phone, full_name=None, password=None):
        """
        Create and save a regular user with the given phone and full_name.
        """
        if not phone:
            raise ValueError('Phone number is required')

        user = self.model(
            phone=self.normalize_phone(phone),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name="Admin", password=None):
        """
        Create and save a superuser with the given phone and password.
        """
        user = self.create_user(
            phone=phone,
            full_name=full_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def normalize_phone(self, phone):
        """
        Normalize phone number by removing spaces and ensuring consistent format.
        """
        return phone.replace(' ', '').strip()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using phone number as the primary identifier.
    """

    # Contact Information
    phone = models.CharField(
        max_length=11,
        unique=True,
        blank=True,
        null=True,
        help_text="Phone number in format: 09xxxxxxxxx"
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        help_text="Optional email address"
    )

    # Profile Information
    full_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="User's full name"
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text="Optional username for card URL"
    )

    # Plan and Subscription
    plan = models.ManyToManyField(
        UserPlan,
        blank=True,
        help_text="User's active subscription plans"
    )
    plan_expires_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When the current plan expires"
    )

    # Django Auth Fields
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active"
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into admin site"
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        help_text="Date when user joined"
    )

    # Audit Fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this user was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this user was last updated"
    )

    # Django Auth Configuration
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']

    def get_remaining_days(self):
        """
        Get remaining days until plan expires.

        Returns:
            int or None: Days remaining, or None if no expiration set
        """
        if not self.plan_expires_at:
            return None

        delta = self.plan_expires_at.date() - timezone.now().date()
        return max(delta.days, 0)

    def is_plan_expiring_soon(self, warning_days=7):
        """
        Check if user's plan is expiring soon.

        Args:
            warning_days (int): Number of days to warn before expiration

        Returns:
            bool: True if plan expires within warning_days
        """
        if not self.plan_expires_at:
            return False

        remaining_time = self.plan_expires_at - timezone.now()
        return remaining_time <= timedelta(days=warning_days)

    def has_plan(self, plan_value):
        """
        Check if user has a specific plan.

        Args:
            plan_value (str): Plan value to check (e.g., 'Basic', 'Pro')

        Returns:
            bool: True if user has the specified plan
        """
        return self.plan.filter(value=plan_value).exists()

    def get_active_plans(self):
        """
        Get list of active plan values.

        Returns:
            list: List of plan values (e.g., ['Basic', 'Pro'])
        """
        return list(self.plan.values_list('value', flat=True))

    def __str__(self):
        """
        String representation of the user.
        """
        if self.full_name:
            return f"{self.full_name} ({self.phone})"
        return f"User {self.phone or self.id}"


class OTP(models.Model):
    """
    One-Time Password model for user authentication.
    """

    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="otps",
        help_text="User this OTP belongs to"
    )
    code = models.CharField(
        max_length=6,
        help_text="6-digit OTP code"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this OTP was created"
    )
    expires_at = models.DateTimeField(
        help_text="When this OTP expires"
    )

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'expires_at']),
            models.Index(fields=['expires_at']),
        ]

    def is_expired(self):
        """
        Check if this OTP has expired.

        Returns:
            bool: True if current time is past expiration time
        """
        return timezone.now() > self.expires_at

    def is_valid(self):
        """
        Check if this OTP is valid (not expired).

        Returns:
            bool: True if OTP is still valid
        """
        return not self.is_expired()

    def get_time_remaining(self):
        """
        Get remaining time before expiration.

        Returns:
            timedelta or None: Time remaining, or None if expired
        """
        if self.is_expired():
            return None

        return self.expires_at - timezone.now()

    def __str__(self):
        """
        String representation of the OTP.
        """
        return f"OTP for {self.user.phone}: {self.code}"
