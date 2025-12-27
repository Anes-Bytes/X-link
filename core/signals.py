from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserPlan

@receiver(post_save, sender=CustomUser)
def assign_free_plan(sender, instance, created, **kwargs):
    if created:
        try:
            free_plan = UserPlan.objects.get(value=UserPlan.PlanChoices.Free)
            instance.plan.add(free_plan)
        except UserPlan.DoesNotExist:
            # Free plan doesn't exist yet, skip silently in tests
            pass
