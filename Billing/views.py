from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render
from django.contrib import messages
from site_management.models import Customers
from .models import Plan, Template


def landing_view(request):
    period = request.GET.get("period", Plan.PeriodChoices.MONTHLY)

    if period not in (
        Plan.PeriodChoices.MONTHLY,
        Plan.PeriodChoices.ANNUAL,
    ):
        period = Plan.PeriodChoices.MONTHLY

    plans_cache_key = f"landing_plans_{period}"
    plans = cache.get(plans_cache_key)

    if plans is None:
        plans = list(
            Plan.objects
            .select_related("discount")
            .prefetch_related("Features")
            .filter(period=period)
        )
        cache.set(plans_cache_key, plans, 60 * 15)

    templates = cache.get("landing_templates")

    if templates is None:
        templates = list(
            Template.objects.filter(is_active=True)
        )
        cache.set("landing_templates", templates, 60 * 60)

    customers = cache.get("landing_customers")

    if customers is None:
        customers = list(Customers.objects.all())
        cache.set("landing_customers", customers, 60 * 60)

    return render(
        request,
        "Billing/landing.html",
        {
            "templates": templates,
            "customers": customers,
            "Billing": plans,
            "current_period": period,
        }
    )


def pricing_view(request):
    period = request.GET.get("period")
    if period == "monthly":
        plans = list(Plan.objects.select_related("discount").prefetch_related("Features").filter(period=Plan.PeriodChoices.MONTHLY))
    elif period == "annual":
        plans = list(Plan.objects.select_related("discount").prefetch_related("Features").filter(period=Plan.PeriodChoices.ANNUAL))
    else:
        plans = list(Plan.objects.select_related("discount").prefetch_related("Features").filter(period=Plan.PeriodChoices.MONTHLY))

    return render(request, 'Billing/pricing.html', context={'Billing': plans, "current_period": period,})

@login_required
def payment_success_view(request):
    messages.success(request, "با تشکر از اعتماد شما")
    return render(request, 'Billing/payment-success.html')

@login_required
def payment_failed_view(request):
    messages.error(request, "خطایی در هنگام پرداخت رخ داده است. مجددا تلاش کنید")
    return render(request, 'Billing/payment-failed.html')

def about_view(request):
    """
    About Us page for X-link
    """
    return render(request, 'Billing/about.html')
