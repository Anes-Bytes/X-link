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
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, related_name='Features')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Plan(models.Model):
    class TypeChoices(models.TextChoices):
        Free = "Free", "Free"
        Basic = "Basic", "Basic"
        Pro = "Pro", "Pro"

    class PeriodChoices(models.TextChoices):
        MONTHLY = "monthly", "ماهانه"
        ANNUAL = "annual", "سالانه"

    type = models.CharField(max_length=20, choices=TypeChoices.choices)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='+')
    is_special = models.BooleanField()
    period = models.CharField(max_length=20, choices=PeriodChoices.choices, default="monthly")

    def get_final_price(self):
        if not self.discount:
            return self.price
        return max(self.price * (1 - self.discount.value / 100), 0)

    def __str__(self):
        return self.name


class Template(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='templates')
    description = models.TextField(blank=True)
    delay = models.IntegerField()
    only_for_premium = models.BooleanField(default=False)
    allowed_plans = models.ManyToManyField(UserPlan, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
