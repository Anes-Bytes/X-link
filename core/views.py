import logging
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET, require_POST
from environs import Env
from melipayamak import Api

from cards.models import UserCard
from core.models import CustomUser
from core.serializers import SubdomainAvailabilitySerializer
from core.services.subdomains import assign_subdomain_to_user, check_subdomain_availability
from shop.models import UserShop
from .forms import UserLoginForm, UserSignupForm
from .signals import user_registered
from .utils import get_client_ip

logger = logging.getLogger(__name__)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            requested_subdomain = form.cleaned_data["username"]
            check = check_subdomain_availability(requested_subdomain)
            if not check.available:
                form.add_error("username", f"Subdomain error: {check.reason}")
                return render(request, "core/login.html", {"form": form, "active_tab": "signup"})

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            assign_subdomain_to_user(user, requested_subdomain)

            ip = get_client_ip(request)
            user_registered.send(
                sender=user.__class__,
                user=user,
                request=request,
                ip_address=ip,
                event_type="registration",
            )

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "ثبت نام با موفقیت انجام شد. خوش آمدید!")
            return redirect("dashboard")
    else:
        form = UserSignupForm()

    return render(request, "core/login.html", {"form": form, "active_tab": "signup"})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    next_page = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید")

            if next_page and url_has_allowed_host_and_scheme(next_page, allowed_hosts={request.get_host()}):
                return redirect(next_page)
            return redirect("dashboard")
    else:
        form = UserLoginForm()

    return render(request, "core/login.html", {"form": form, "next": next_page})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "شما با موفقیت خارج شدید.")
    return redirect("home")


@login_required
def dashboard_view(request):
    user_card = UserCard.objects.filter(user=request.user).first()
    user_shops = list(UserShop.objects.filter(user=request.user).prefetch_related("products"))

    card_url = None
    user_subdomain = getattr(request.user, "subdomain", None)
    if user_card and user_subdomain and user_subdomain.is_active:
        scheme = "https" if request.is_secure() else "http"
        card_url = f"{scheme}://{user_subdomain.subdomain}.{request.get_host()}"

    user_plans = set(request.user.plan.values_list("value", flat=True))
    has_basic_plan = "Basic" in user_plans
    has_pro_plan = "Pro" in user_plans
    has_free_plan = "Free" in user_plans
    can_create_more_shops = has_basic_plan or has_pro_plan or len(user_shops) == 0

    context = {
        "user_card": user_card,
        "user_shops": user_shops,
        "card_url": card_url,
        "user_subdomain_name": user_subdomain.subdomain if user_subdomain else "",
        "can_create_more_shops": can_create_more_shops,
        "has_basic_plan": has_basic_plan,
        "has_pro_plan": has_pro_plan,
        "has_free_plan": has_free_plan,
    }

    return render(request, "core/dashboard.html", context)


@require_GET
def check_subdomain_view(request):
    name = request.GET.get("name", "")
    user = request.user if request.user.is_authenticated else None
    result = check_subdomain_availability(name, user=user)
    return JsonResponse(SubdomainAvailabilitySerializer.serialize(result))
