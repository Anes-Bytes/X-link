from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver, Signal
from .models import CustomUser
from Billing.models import UserPlan
from bot.notifier import send_telegram_notification
import logging

logger = logging.getLogger(__name__)


user_registered = Signal()
user_card_created = Signal()
admin_accessed = Signal()
backup_completed = Signal()

@receiver(post_save, sender=CustomUser)
def notify_new_user(sender, instance, created, **kwargs):
    if created:
        # Assign free plan
        try:
            free_plan = UserPlan.objects.get(value=UserPlan.PlanChoices.Free)
            instance.plan.add(free_plan)
        except UserPlan.DoesNotExist:
            pass
        
        # Send Telegram notification
        msg = (
            "🆕 **ثبت نام کاربر جدید**\n\n"
            f"👤 نام: {instance.full_name or 'N/A'}\n"
            f"📞 شماره: {instance.phone}\n"
            f"📧 ایمیل: {instance.email or 'N/A'}"
        )
        send_telegram_notification(msg)

@receiver(user_logged_in)
def notify_user_login(sender, request, user, **kwargs):
    msg = (
        "🔑 **ورود کاربر**\n\n"
        f"👤 کاربر: {user.full_name or user.phone}\n"
        f"⏰ زمان: {user.last_login.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    send_telegram_notification(msg)
