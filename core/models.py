from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from datetime import datetime, timedelta

from Billing.models import *
from site_management.models import *

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


class UserMessages(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = ["full_name"]

    plan = models.ManyToManyField(UserPlan, blank=True)
    plan_expires_at = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def plan_expires(self):
        if not self.plan_expires_at:
            return None
        delta = self.plan_expires_at.date() - timezone.now().date()
        return max(delta.days, 0)


    def is_expires_soon(self):
        if not self.plan_expires_at:
            return False

        now = datetime.now()

        remaining = self.plan_expires_at - now

        return remaining <= timedelta(days=8)

    def __str__(self):
        return self.full_name if self.full_name else str(self.id)


class OTP(models.Model):
    user = models.ForeignKey("core.CustomUser", on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.phone} - {self.code}"



