from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render
from django.contrib import messages
from site_management.models import Customer
from django.views.decorators.cache import cache_page
from .models import Plan, Template

def landing_view(request):
    period = request.GET.get("period", Plan.Period.MONTHLY)

    if period not in (
        Plan.Period.MONTHLY,
        Plan.Period.ANNUAL,
    ):
        period = Plan.Period.MONTHLY

    cache_key = f"landing_data_{period}"
    data = cache.get(cache_key)

    if data is None:
        plans = list(
            Plan.objects
            .select_related("discount")
            .prefetch_related("features")
            .filter(period=period)
        )
        templates = list(Template.objects.filter(is_active=True))
        customers = list(Customer.objects.filter(is_active=True))
        
        data = {
            "plans": plans,
            "templates": templates,
            "customers": customers,
        }
        cache.set(cache_key, data, 60 * 15)

    context = {
        **data,
        "current_period": period,
    }

    return render(
        request,
        "Billing/landing.html",
        context
    )


def pricing_view(request):
    period = request.GET.get("period", Plan.Period.MONTHLY)
    if period not in (Plan.Period.MONTHLY, Plan.Period.ANNUAL):
        period = Plan.Period.MONTHLY
    
    plans_cache_key = f"pricing_plans_{period}"
    plans = cache.get(plans_cache_key)
    
    if plans is None:
        plans = list(Plan.objects.select_related("discount").prefetch_related("features").filter(period=period))
        cache.set(plans_cache_key, plans, 60 * 15)

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

def buy_telegram_view(request):
    """
    Page for purchasing subscription via Telegram
    """
    return render(request, 'Billing/buy_telegram.html')
