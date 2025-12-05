from django.shortcuts import render

from core.models import Customers, Plan
from Xlink.models import CardTemplate


def landing_view(request):
    return render(
        request,
        "xlink/landing.html",
        {
            "templates": CardTemplate.objects.filter(is_active=True),
            "customers": Customers.objects.all(),
            "plans": Plan.objects.all(),
        }
    )