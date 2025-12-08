from django.shortcuts import render
from django.core.cache import cache

from core.models import Customers, Plan
from Xlink.models import CardTemplate


def landing_view(request):
    templates = cache.get("landing_templates")
    customers = cache.get("landing_customers")
    plans = cache.get("landing_plans")

    if templates is None:
        templates = list(CardTemplate.objects.filter(is_active=True))
        cache.set("landing_templates", templates, 60 * 60)

    if customers is None:
        customers = list(Customers.objects.all())
        cache.set("landing_customers", customers, 60 * 60)

    if plans is None:
        plans = list(Plan.objects.select_related("discount").prefetch_related("Features").all())
        cache.set("landing_plans", plans, 60 * 60)

    return render(
        request,
        "xlink/landing.html",
        {
            "templates": templates,
            "customers": customers,
            "plans": plans,
        }
    )
