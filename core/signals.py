from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserPlan

@receiver(post_save, sender=CustomUser)
def assign_pro_plan(sender, instance, created, **kwargs):
    if created:
        try:
            pro_plan = UserPlan.objects.get(value=UserPlan.PlanChoices.Free)
            instance.plan.add(pro_plan)
        except UserPlan.DoesNotExist:
            print("پلن Pro هنوز در دیتابیس ساخته نشده است.")
