import logging

# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.http import url_has_allowed_host_and_scheme
from datetime import timedelta

# Third-party imports
from melipayamak import Api
from environs import Env

# Local app imports
from cards.models import UserCard
from core.models import CustomUser
from .forms import UserSignupForm, UserLoginForm
from .utils import get_client_ip
from .signals import user_registered

# Logger setup
logger = logging.getLogger(__name__)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Send registration signal
            ip = get_client_ip(request)

            user_registered.send(
                sender=user.__class__,
                user=user,
                request=request,
                ip_address=ip,
                event_type='registration'
            )

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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

            if next_page and url_has_allowed_host_and_scheme(
                next_page,
                allowed_hosts={request.get_host()}
            ):
                return redirect(next_page)
            return redirect("dashboard")
    else:
        form = UserLoginForm()

    return render(request, "core/login.html", {"form": form, "next": next_page})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "شما با موفقیت خارج شدید.")
    return redirect('home')

@login_required
def dashboard_view(request):
    user_card = UserCard.objects.filter(user=request.user).first()

    card_url = None
    if user_card and user_card.username:
        scheme = "https" if request.is_secure() else "http"
        card_url = f"{scheme}://{request.get_host()}/{user_card.username}"

    # Get all plan values in one query
    user_plans = set(request.user.plan.values_list('value', flat=True))

    context = {
        "user_card": user_card,
        "card_url": card_url,
        'has_basic_plan': 'Basic' in user_plans,
        'has_pro_plan': 'Pro' in user_plans,
        'has_free_plan': 'Free' in user_plans,
    }

    return render(request, "core/dashboard.html", context)




