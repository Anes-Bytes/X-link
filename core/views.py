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
from cards.models import *
from core.models import CustomUser, OTP

# Logger setup
logger = logging.getLogger(__name__)

# Env setup
env = Env()
env.read_env()


def send_sms(phone: str, code: str) -> bool:
    """
    Send OTP SMS via Melipayamak
    """
    try:
        username = env("MELIPAYAMAK_USERNAME")
        password = env("MELIPAYAMAK_APIKEY")
        sender = env("MELIPAYAMAK_NUMBER")

        api = Api(username, password)
        sms = api.sms()

        text = (
            "کد تایید ایکس لینک\n\n"
            f"کد شما: {code}\n\n"
            "توجه: این کد محرمانه است. آن را در اختیار دیگران قرار ندهید.\n\n"
            "لغو 11"
        )

        sms.send(phone, sender, text)
        return True

    except Exception as e:
        logger.error("SMS send failed for %s: %s", phone, e)
        return False

def request_otp(request):
    if request.method == 'GET':
        return render(request, "core/login.html")

    # POST request handling
    phone = request.POST.get("phone", "").strip()
    full_name = request.POST.get("full_name", "").strip()
    next_page = request.POST.get("next")

    # Validate phone number format
    if not phone:
        messages.error(request, "شماره تلفن الزامی است")
        return redirect("request_otp")

    # Basic phone number validation (Iranian mobile numbers)
    import re
    if not re.match(r'^09\d{9}$', phone):
        messages.error(request, "شماره تلفن باید با 09 شروع شود و 11 رقم باشد")
        return redirect("request_otp")

    # Check if it's signup (has full_name) or login
    is_signup = bool(full_name)

    if is_signup:
        # Signup validation
        if len(full_name) < 2:
            messages.error(request, "نام کامل باید حداقل ۲ حرف باشد")
            return redirect("login")

        # Check if user already exists
        if CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, "این شماره تلفن قبلاً ثبت نام کرده است. از قسمت ورود استفاده کنید")
            return redirect("login")
    else:
        # Login validation
        if not CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, "این شماره تلفن ثبت نشده است. ابتدا ثبت نام کنید")
            return redirect("login")

    # Rate limiting check
    cache_key = f"otp_request_{phone}"
    if cache.get(cache_key):
        messages.error(request, "لطفاً ۶۰ ثانیه صبر کنید و دوباره تلاش کنید")
        return redirect("login")

    cache.set(cache_key, True, timeout=60)

    # Create or get user
    try:
        user = CustomUser.objects.get(phone=phone)
        created = False

        if is_signup and full_name and user.full_name != full_name:
            user.full_name = full_name
            user.save()

    except CustomUser.DoesNotExist:
        # Create new user
        user = CustomUser.objects.create_user(
            phone=phone,
            full_name=full_name if is_signup else None
        )
        created = True

        # Send registration signal if this is a signup
        if is_signup:
            # Get IP address
            if hasattr(request, 'META') and 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
            elif hasattr(request, 'META') and 'REMOTE_ADDR' in request.META:
                ip = request.META['REMOTE_ADDR']
            else:
                ip = 'unknown'

            from .signals import user_registered
            user_registered.send(
                sender=user.__class__,
                user=user,
                request=request,
                ip_address=ip,
                event_type='registration'
            )

    # Expire previous OTPs
    user.otps.filter(expires_at__gt=timezone.now()).update(expires_at=timezone.now())

    # Generate new OTP
    code = get_random_string(6, allowed_chars="0123456789")

    OTP.objects.create(
        user=user,
        code=code,
        expires_at=timezone.now() + timedelta(minutes=2)
    )

    request.session["otp_phone"] = phone
    request.session["is_signup"] = is_signup
    if next_page:
        request.session["next"] = next_page

    try:
        send_sms(phone, code)
        if is_signup:
            messages.success(request, f"کد تایید برای ثبت نام به شماره {phone} ارسال شد")
        else:
            messages.success(request, f"کد تایید برای ورود به شماره {phone} ارسال شد")
    except Exception as e:
        messages.error(request, "خطا در ارسال پیامک. لطفاً دوباره تلاش کنید")
        return redirect("request_otp")

    return redirect("verify_otp")

def verify_otp(request):
    phone = request.session.get("otp_phone")
    next_page = request.session.get("next")

    if request.method == "GET":
        if not phone:
            return redirect("request_otp")
        return render(request, "core/verify.html")

    # -------- POST --------
    code = request.POST.get("code", "").strip()

    if not phone or not code:
        messages.error(request, "اطلاعات نامعتبر است")
        return redirect("request_otp")

    user = get_object_or_404(CustomUser, phone=phone)

    otp = user.otps.filter(
        code=code,
        expires_at__gt=timezone.now()
    ).last()

    if not otp:
        messages.error(request, "کد اشتباه یا منقضی شده")
        return redirect("verify_otp")

    otp.delete()
    login(request, user)
    messages.success(request, "با موفقیت وارد شدید")

    if next_page and url_has_allowed_host_and_scheme(
        next_page,
        allowed_hosts={request.get_host()}
    ):
        request.session.pop("next", None)
        return redirect(next_page)
    messages.success(request, "خوش آمدید")
    return redirect("dashboard")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    next_page = request.GET.get("next")

    if next_page and not url_has_allowed_host_and_scheme(
        next_page,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_page = None

    return render(
        request,
        "core/login.html",
        {
            "next": next_page,
        }
    )

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "شما با موفقیت خارج شدید.")
    return redirect('home')

@login_required
def dashboard_view(request):
    user_card = UserCard.objects.filter(user=request.user).select_related('user').first()

    card_url = None
    if user_card and user_card.username:
        scheme = "https" if request.is_secure() else "http"
        card_url = f"{scheme}://{request.get_host()}/{user_card.username}"

    user_plans = set(request.user.plan.values_list('value', flat=True))

    context = {
        "user_card": user_card,
        "card_url": card_url,
        'has_basic_plan': 'Basic' in user_plans,
        'has_pro_plan': 'Pro' in user_plans,
        'has_free_plan': 'Free' in user_plans,
    }

    return render(request, "core/dashboard.html", context)




