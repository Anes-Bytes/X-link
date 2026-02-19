from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from .models import CustomUser, UserPlan

# Signal sent when a new user is registered via custom signup view
user_registered = Signal()

@receiver(post_save, sender=CustomUser)
def assign_free_plan(sender, instance, created, **kwargs):
    """
    Assign Free plan to newly created users with unlimited duration.
    """
    if created:
        try:
            free_plan, _ = UserPlan.objects.get_or_create(value='Free')
            instance.plan.add(free_plan)
            
            # Use update to avoid re-triggering signals and for better performance
            CustomUser.objects.filter(id=instance.id).update(plan_expires_at=None)
        except Exception as e:
            print(f"Error assigning free plan to user {instance.username}: {e}")
