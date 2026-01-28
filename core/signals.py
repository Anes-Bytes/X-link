from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import CustomUser
from cards.models import UserCard
from .utils import send_telegram_notification

@receiver(post_save, sender=CustomUser)
def notify_signup(sender, instance, created, **kwargs):
    if created:
        send_telegram_notification(f"🆕 کاربر جدید ثبت‌نام کرد:\n👤 نام: {instance.full_name or 'نامشخص'}\n📞 شماره: {instance.phone or 'نامشخص'}")

@receiver(user_logged_in)
def notify_login(sender, request, user, **kwargs):
    send_telegram_notification(f"👤 کاربر `{user.full_name or user.phone}` وارد سیستم شد.")

@receiver(post_save, sender=UserCard)
def notify_card_creation(sender, instance, created, **kwargs):
    if created:
        send_telegram_notification(f"🏗 کارت جدید ایجاد شد:\n👤 مالک: {instance.name}\n🔗 آیدی: @{instance.username}")
