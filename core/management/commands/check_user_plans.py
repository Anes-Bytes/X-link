from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from core.models import CustomUser, UserPlan
from cards.models import UserCard


class Command(BaseCommand):
    help = 'Check user Billing and update expired Billing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )

        # Get current time
        now = timezone.now()

        # Find users with expired Billing
        expired_users = CustomUser.objects.filter(
            plan_expires_at__lt=now
        ).exclude(
            plan_expires_at__isnull=True
        ).prefetch_related('plan')

        if not expired_users.exists():
            self.stdout.write(
                self.style.SUCCESS('No expired Billing found.')
            )
            return

        # Process expired users
        processed_count = 0
        for user in expired_users:
            user_plans = list(user.plan.all())
            plan_names = [plan.get_value_display() for plan in user_plans]

            if dry_run:
                self.stdout.write(
                    f'Would expire Billing for user {user.full_name or user.phone}: '
                    f'{", ".join(plan_names)} → Would add Free plan (expired: {user.plan_expires_at})'
                )
            else:
                # Remove all Billing from expired user
                user.plan.clear()

                # Add Free plan to expired user
                try:
                    free_plan, _ = UserPlan.objects.get_or_create(value='Free')
                    user.plan.add(free_plan)
                    user.plan_expires_at = None
                    user.save()

                    # Reset premium card features
                    try:
                        card = user.user_card
                        card.black_background = False
                        card.stars_background = False
                        card.blue_tick = False
                        card.color = 'default'
                        card.save()
                    except UserCard.DoesNotExist:
                        pass

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Expired Billing for user {user.full_name or user.phone}: '
                            f'{", ".join(plan_names)} → Added Free plan and reset features'
                        )
                    )
                except Exception as e:
                    # If error occurred, just clear Billing
                    user.plan_expires_at = None
                    user.save()

                    self.stdout.write(
                        self.style.ERROR(
                            f'Expired Billing for user {user.full_name or user.phone}: '
                            f'{", ".join(plan_names)} → Error: {e}'
                        )
                    )

            processed_count += 1

        # Show summary
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would process {processed_count} users with expired Billing'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed {processed_count} users with expired Billing'
                )
            )

        # Show users expiring soon (next 7 days)
        soon_expiring = CustomUser.objects.filter(
            plan_expires_at__gte=now,
            plan_expires_at__lte=now + timezone.timedelta(days=7)
        ).exclude(
            plan_expires_at__isnull=True
        ).prefetch_related('plan')

        if soon_expiring.exists():
            self.stdout.write('\nUsers with Billing expiring soon:')
            for user in soon_expiring:
                days_left = (user.plan_expires_at.date() - now.date()).days
                user_plans = list(user.plan.all())
                plan_names = [plan.get_value_display() for plan in user_plans]

                self.stdout.write(
                    self.style.WARNING(
                        f'{user.full_name or user.phone}: {", ".join(plan_names)} '
                        f'(expires in {days_left} days - {user.plan_expires_at.date()})'
                    )
                )
