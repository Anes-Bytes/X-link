import json
import datetime
import logging

# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import F

# Third-party imports
from melipayamak import Api
from environs import Env

# Local app imports
from .models import UserCard, Skill, Service, Portfolio, Template, Customers, Plan
from .forms import UserCardForm, SkillInlineFormSet, ServiceInlineFormSet, PortfolioInlineFormSet
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

@require_POST
def request_otp(request):
    phone = request.POST.get("phone", "").strip()
    full_name = request.POST.get("full_name", "").strip()
    next_page = request.POST.get("next")

    if not phone:
        messages.error(request, "شماره تلفن معتبر نیست")
        return redirect("request_otp")

    cache_key = f"otp_request_{phone}"
    if cache.get(cache_key):
        messages.error(request, "لطفاً کمی بعد دوباره تلاش کنید")
        return redirect("request_otp")

    cache.set(cache_key, True, timeout=60)

    user, _ = CustomUser.objects.get_or_create(
        phone=phone,
        defaults={"full_name": full_name}
    )

    user.otps.filter(expires_at__gt=timezone.now()).update(expires_at=timezone.now())

    code = get_random_string(6, allowed_chars="0123456789")

    OTP.objects.create(
        user=user,
        code=code,
        expires_at=timezone.now() + datetime.timedelta(minutes=2)
    )

    request.session["otp_phone"] = phone
    if next_page:
        request.session["next"] = next_page

    send_sms(phone, code)
    messages.success(request, "کد تایید ارسال شد")
    return redirect("verify_otp")

@require_POST
def verify_otp(request):
    phone = request.session.get("otp_phone")
    code = request.POST.get("code", "").strip()
    next_page = request.session.get("next")

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
        del request.session["next"]
        return redirect(next_page)

    return redirect("dashboard")

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
        "core/landing.html",
        {
            "templates": templates,
            "customers": customers,
            "plans": plans,
            "current_period": period,
        }
    )

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
    username = request.user.username
    logout(request)
    messages.success(request, "شما با موفقیت خارج شدید.")
    logger.info("User logged out: %s", username)
    return redirect('login')

@login_required
def dashboard_view(request):
    user_card = UserCard.objects.filter(user=request.user).first()

    card_url = None
    if user_card and user_card.username:
        scheme = "https" if request.is_secure() else "http"
        card_url = f"{scheme}://{request.get_host()}/{user_card.username}"

    user_plans = set(request.user.plan.values_list('name', flat=True))

    context = {
        "user_card": user_card,
        "card_url": card_url,
        'has_basic_plan': 'Basic' in user_plans,
        'has_pro_plan': 'Pro' in user_plans,
        'has_free_plan': 'Free' in user_plans,
        'messages':request.user.messages.all(),
    }

    return render(request, "core/dashboard.html", context)

@login_required
def card_builder_view(request):
    user_card, is_new = UserCard.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserCardForm(request.POST, request.FILES, instance=user_card)
        skill_formset = SkillInlineFormSet(request.POST, instance=user_card, prefix='skill')
        service_formset = ServiceInlineFormSet(request.POST, instance=user_card, prefix='service')
        portfolio_formset = PortfolioInlineFormSet(request.POST, request.FILES, instance=user_card, prefix='portfolio')

        if form.is_valid() and skill_formset.is_valid() and service_formset.is_valid() and portfolio_formset.is_valid():
            card = form.save(commit=False)
            card.user = request.user

            if request.user.plan.filter(name="Pro").exists():
                card.black_background = bool(request.POST.get("black_bg"))
                card.stars_background = bool(request.POST.get("stars_bg"))
                card.blue_tick = bool(request.POST.get("blue_tick"))

            card.save()
            skill_formset.instance = card
            skill_formset.save()
            service_formset.instance = card
            service_formset.save()
            portfolio_formset.instance = card
            portfolio_formset.save()

            logger.info("Card saved for user %s, card_id=%s", request.user.username, card.id)
            return redirect('card_success', card_id=card.id)
        else:
            logger.warning("Card form validation failed for user %s", request.user.username)
            logger.debug("Form errors: %s", form.errors)
            logger.debug("Skill errors: %s", skill_formset.errors)
            logger.debug("Service errors: %s", service_formset.errors)
            logger.debug("Portfolio errors: %s", portfolio_formset.errors)

    else:
        form = UserCardForm(instance=user_card)
        skill_formset = SkillInlineFormSet(instance=user_card, prefix='skill')
        service_formset = ServiceInlineFormSet(instance=user_card, prefix='service')
        portfolio_formset = PortfolioInlineFormSet(instance=user_card, prefix='portfolio')

    templates = Template.objects.filter(is_active=True).prefetch_related('allowed_plans')
    user_plans_set = set(request.user.plan.values_list('name', flat=True))

    template_access = {
        template.id: template.allowed_plans.filter(id__in=request.user.plan.all()).exists()
        for template in templates
    }

    context = {
        'form': form,
        'skill_formset': skill_formset,
        'service_formset': service_formset,
        'portfolio_formset': portfolio_formset,
        'templates': templates,
        'template_access': template_access,
        'is_new': is_new,
        'has_pro_plan': 'Pro' in user_plans_set,
    }

    return render(request, 'core/card_builder.html', context)

@login_required
def card_success_view(request, card_id):
    user_card = get_object_or_404(
        UserCard.objects.prefetch_related("skills", "services", "portfolio_items"),
        id=card_id,
        user=request.user
    )
    card_url = user_card.get_card_url()

    logger.info("Card success page viewed by user %s for card_id=%s", request.user.username, card_id)

    return render(request, 'core/card_success.html', {
        'user_card': user_card,
        'card_url': card_url,
    })

def view_card(request, username):
    user_card = get_object_or_404(
        UserCard.objects.prefetch_related("skills", "services", "portfolio_items"),
        username=username,
        is_published=True
    )

    UserCard.objects.filter(id=user_card.id).update(views=F('views') + 1)

    context = {
        'user_card': user_card,
    }

    return render(request, 'core/card_view.html', context)


@require_http_methods(["POST"])
@login_required
def add_skill_ajax(request):
    """AJAX endpoint to add a new skill dynamically"""
    try:
        data = json.loads(request.body)
        skill_name = data.get('name', '').strip()

        if not skill_name:
            return JsonResponse({'error': 'Skill name is required'}, status=400)

        user_card = UserCard.objects.get(user=request.user)
        skill = Skill.objects.create(user_card=user_card, name=skill_name)

        return JsonResponse({
            'success': True,
            'skill': {
                'id': skill.id,
                'name': skill.name,
            }
        })
    except UserCard.DoesNotExist:
        return JsonResponse({'error': 'User card not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["DELETE"])
@login_required
def delete_skill_ajax(request, skill_id):
    """AJAX endpoint to delete a skill"""
    try:
        skill = get_object_or_404(Skill, id=skill_id, user_card__user=request.user)
        skill.delete()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def add_service_ajax(request):
    """AJAX endpoint to add a new service dynamically"""
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()

        if not title:
            return JsonResponse({'error': 'Service title is required'}, status=400)

        user_card = UserCard.objects.get(user=request.user)
        service = Service.objects.create(
            user_card=user_card,
            title=title,
            description=data.get('description', '')
        )

        return JsonResponse({
            'success': True,
            'service': {
                'id': service.id,
                'title': service.title,
                'description': service.description,
                'icon': service.icon,
            }
        })
    except UserCard.DoesNotExist:
        return JsonResponse({'error': 'User card not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["DELETE"])
@login_required
def delete_service_ajax(request, service_id):
    """AJAX endpoint to delete a service"""
    try:
        service = get_object_or_404(Service, id=service_id, user_card__user=request.user)
        service.delete()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@require_http_methods(["DELETE"])
@login_required
def delete_portfolio_ajax(request, portfolio_id):
    """AJAX endpoint to delete a portfolio item"""
    try:
        portfolio = get_object_or_404(Portfolio, id=portfolio_id, user_card__user=request.user)
        portfolio.delete()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def pricing_view(request):
    period = request.GET.get("period")
    if period == "monthly":
        plans = list(Plan.objects.select_related("discount").prefetch_related("Features").filter(period=Plan.PeriodChoices.MONTHLY))
    elif period == "annual":
        plans = list(Plan.objects.select_related("discount").prefetch_related("Features").filter(period=Plan.PeriodChoices.ANNUAL))
    else:
        plans = list(Plan.objects.select_related("discount").prefetch_related("Features").filter(period=Plan.PeriodChoices.MONTHLY))



    return render(request, 'core/pricing.html', context={'plans': plans, "current_period": period,})

@login_required
def payment_success_view(request):
    return render(request, 'core/payment-success.html')

@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')
