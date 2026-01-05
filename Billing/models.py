from django.db import models

class UserPlan(models.Model):
    class PlanChoices(models.TextChoices):
        Free = "Free", "رایگان"
        Basic = "Basic", "پلن پایه"
        Pro = "Pro", "پرمیوم"
    value = models.CharField(choices=PlanChoices.choices, max_length=20)

    def __str__(self):
        return self.value


class Discount(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return f"{self.value}%"


class Feature(models.Model):
    """
    Feature included in a subscription plan.
    """

    plan = models.ForeignKey(
        'Plan',
        on_delete=models.CASCADE,
        related_name='features',
        help_text="Plan this feature belongs to"
    )
    name = models.CharField(
        max_length=200,
        help_text="Name of the feature"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this feature was created"
    )

    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"
        ordering = ['name']
        unique_together = ['plan', 'name']

    def __str__(self):
        return self.name


class Plan(models.Model):
    """
    Subscription plan with pricing and features.
    """

    class PlanType(models.TextChoices):
        FREE = "Free", "رایگان"
        BASIC = "Basic", "پایه"
        PRO = "Pro", "حرفه‌ای"

    class Period(models.TextChoices):
        MONTHLY = "monthly", "ماهانه"
        ANNUAL = "annual", "سالانه"

    plan_type = models.CharField(
        max_length=20,
        choices=PlanType.choices,
        help_text="Type of subscription plan"
    )
    name = models.CharField(
        max_length=200,
        help_text="Display name of the plan"
    )
    price = models.PositiveIntegerField(
        help_text="Base price in IRR (Rials)"
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='plans',
        help_text="Discount applied to this plan"
    )
    is_special = models.BooleanField(
        default=False,
        help_text="Whether this is a special/recommended plan"
    )
    period = models.CharField(
        max_length=20,
        choices=Period.choices,
        default=Period.MONTHLY,
        help_text="Billing period for this plan"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this plan is currently available"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this plan was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this plan was last updated"
    )

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ['price']
        unique_together = ['plan_type', 'period']

    def get_discounted_price(self):
        """
        Calculate the final price after applying discount.

        Returns:
            int: Final price in IRR
        """
        if not self.discount:
            return self.price

        discount_amount = self.price * (self.discount.value / 100)
        return max(int(self.price - discount_amount), 0)

    def get_savings_percentage(self):
        """
        Get the percentage saved compared to original price.

        Returns:
            int: Savings percentage (0-100)
        """
        if not self.discount:
            return 0

        return self.discount.value

    def get_savings_amount(self):
        """
        Get the amount saved in IRR.

        Returns:
            int: Savings amount in IRR
        """
        if not self.discount:
            return 0

        return self.price - self.get_discounted_price()

    def is_free(self):
        """
        Check if this is a free plan.

        Returns:
            bool: True if plan is free
        """
        return self.plan_type == self.PlanType.FREE

    def __str__(self):
        """
        String representation of the plan.
        """
        period_display = dict(self.Period.choices)[self.period]
        return f"{self.name} - {period_display}"


class Template(models.Model):
    """
    Card template with styling and access control.
    """

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Template name"
    )
    image = models.ImageField(
        upload_to='templates',
        help_text="Template preview image"
    )
    description = models.TextField(
        blank=True,
        help_text="Template description"
    )
    delay = models.PositiveIntegerField(
        default=0,
        help_text="Animation delay in milliseconds"
    )
    allowed_plans = models.ManyToManyField(
        UserPlan,
        blank=True,
        related_name='allowed_templates',
        help_text="Plans that can use this template (empty = all plans)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this template is available for use"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this template was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this template was last updated"
    )

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"
        ordering = ['name']

    def is_allowed_for_plan(self, plan_value):
        """
        Check if this template is allowed for a specific plan.

        Args:
            plan_value (str): Plan value to check

        Returns:
            bool: True if template is allowed for the plan
        """
        # If no plans specified, template is available to all
        if not self.allowed_plans.exists():
            return True

        return self.allowed_plans.filter(value=plan_value).exists()

    def get_allowed_plan_values(self):
        """
        Get list of plan values that can use this template.

        Returns:
            list: List of allowed plan values
        """
        if not self.allowed_plans.exists():
            return ['all']

        return list(self.allowed_plans.values_list('value', flat=True))

    def __str__(self):
        """
        String representation of the template.
        """
        status = "فعال" if self.is_active else "غیرفعال"
        return f"{self.name} ({status})"
