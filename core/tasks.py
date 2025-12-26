from django.utils import timezone
from datetime import timedelta
from .models import CustomUser, UserPlan
from .utils import send_sms

@shared_task
def check_all_user_plans():
    now = timezone.now()
    users = CustomUser.objects.filter(plan_expires_at__isnull=False)

    for user in users:
        remaining = user.plan_expires_at - now

        try:
            if remaining <= timedelta(seconds=0):
                # پلن تمام شده → Free
                free_plan, _ = UserPlan.objects.get_or_create(value=UserPlan.PlanChoices.Free)
                user.plan.clear()
                user.plan.add(free_plan)
                user.save()
                send_sms(
                    user,
                    f"مشترک گرامی ,\n\n"
                    f"پلن اشتراک شما در سرویس X-Link به پایان رسیده است.\n"
                    f"اکنون پلن شما به حالت رایگان تغییر پیدا کرده است.\n"
                    f"برای تمدید و استفاده از امکانات ویژه می‌توانید از پنل کاربری خود اقدام کنید.\n\n"
                    f"با احترام، تیم X-Link."
                )
            elif remaining <= timedelta(days=2):
                send_sms(
                    user,
                    f"کاربر گرامی {user.full_name or 'عزیز'},\n\n"
                    f"پلن اشتراک شما کمتر از ۲ روز دیگر منقضی می‌شود.\n"
                    f"برای جلوگیری از توقف امکانات ویژه لطفاً پیش از پایان اعتبار اقدام به تمدید نمایید.\n\n"
                    f"با احترام، تیم X-Link."
                )
            elif remaining <= timedelta(days=7):
                send_sms(
                    user,
                    f"کاربر محترم {user.full_name or 'عزیز'},\n\n"
                    f"پلن اشتراک شما کمتر از ۷ روز دیگر منقضی می‌شود.\n"
                    f"فرصت کافی برای تمدید وجود دارد تا از امکانات ویژه بهره‌مند باشید.\n\n"
                    f"با احترام، تیم X-Link."
                )
        except Exception as e:
            # log error
            print(f"Error checking plan for user {user.id}: {e}")
