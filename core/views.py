from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.cache import cache

import json

from .models import UserCard, Skill, Template, Customers, Plan
from .forms import UserCardForm, SkillInlineFormSet


from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import CustomUser, OTP
from django.utils import timezone
import datetime
import random
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from melipayamak import Api

from environs import Env
env = Env()
env.read_env()

def send_sms(phone, code):
    # username = env("MELIPAYAMAK_USERNAME")
    # password = env("MELIPAYAMAK_APIKEY")
    # api = Api(username, password)
    # sms = api.sms()
    # to = phone
    # _from = env("MELIPAYAMAK_NUMBER")
    # text = f'''کد تایید پرشین گیمز
    #
    # کد شما: {code}
    #
    # توجه: این کد محرمانه است. آن را به هیچ‌کس حتی در صورت ادعای پشتیبانی ندهید.
    #
    # پرشین گیمز
    # لغو 11'''
    #
    # response = sms.send(to, _from, text)
    print(f"{phone}, {code}")

def request_otp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        full_name = request.POST.get("full_name")
        next_page = request.POST.get("next")
        print(phone)
        if next_page:
            request.session["next"] = next_page
        if not phone:
            messages.error(request, "شماره تلفن وارد نشده")
            return redirect("request_otp")

        user, created = CustomUser.objects.get_or_create(phone=phone, defaults={"full_name": full_name})

        code = str(random.randint(100000, 999999))
        OTP.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + datetime.timedelta(minutes=2)
        )
        request.session["phone"] = phone
        request.session.modified = True
        send_sms(phone, code)
        messages.success(request, "کد تایید ارسال شد")
        return redirect("verify_otp")

    return redirect("login")

def verify_otp(request):
    if request.method == "POST":
        phone = request.session.get("phone")
        code = request.POST.get("code")
        next_page = request.session.get("next")  # از session می‌خوانیم

        try:
            user = CustomUser.objects.get(phone=phone)
            otp = user.otps.filter(code=code).last()

            if not otp:
                messages.error(request, "کد اشتباه است")
                return redirect("verify_otp")

            if otp.is_expired():
                messages.error(request, "کد منقضی شده")
                return redirect("request_otp")

            login(request, user)
            messages.success(request, "وارد شدید!")

            # اگر next تنظیم شده بود → همانجا برو
            if next_page:
                del request.session["next"]  # فقط یک بار مصرف
                return redirect(next_page)

            # اگر نبود → صفحه اصلی
            return redirect("home")

        except CustomUser.DoesNotExist:
            messages.error(request, "کاربر وجود ندارد")
            return redirect("request_otp")

    return render(request, "core/verify.html")

def landing_view(request):
    templates = cache.get("landing_templates")
    customers = cache.get("landing_customers")
    plans = cache.get("landing_plans")

    if templates is None:
        templates = list(Template.objects.filter(is_active=True))
        cache.set("landing_templates", templates, 60 * 60)

    if customers is None:
        customers = list(Customers.objects.all())
        cache.set("landing_customers", customers, 60 * 60)

    if plans is None:
        plans = list(Plan.objects.select_related("discount").prefetch_related("Features").all())
        cache.set("landing_plans", plans, 60 * 60)

    return render(
        request,
        "core/landing.html",
        {
            "templates": templates,
            "customers": customers,
            "plans": plans,
        }
    )

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    next_page = request.GET.get("next", "")
    return render(request, "core/login.html", {"next": next_page})

@login_required
def dashboard_view(request):
    user_card = UserCard.objects.filter(user=request.user).first()

    card_url = None
    if user_card:
        card_url = f"https://x-link.ir/{user_card.username}"

    return render(
        request,
        "core/dashboard.html",
        {
            "user_card": user_card,
            "card_url": card_url,
        }
    )

def card_builder_view(request):
    """Main card builder view - handles card creation and editing"""
    try:
        user_card = UserCard.objects.get(user=request.user)
        is_new = False
    except UserCard.DoesNotExist:
        user_card = UserCard(user=request.user)
        is_new = True

    if request.method == 'POST':
        form = UserCardForm(request.POST, request.FILES, instance=user_card)
        formset = SkillInlineFormSet(request.POST, instance=user_card)

        if form.is_valid() and formset.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            if request.user.plan == CustomUser.UserPlan.PRO:
                card.black_background = bool(request.POST.get("black_bg"))
                card.stars_background = bool(request.POST.get("stars_bg"))
                card.blue_tick = bool(request.POST.get("blue_tick"))
            card.save()

            formset.instance = card
            formset.save()

            # Redirect to success page
            return redirect('card_success', card_id=card.id)
    else:
        form = UserCardForm(instance=user_card)
        formset = SkillInlineFormSet(instance=user_card) if not is_new else SkillInlineFormSet()

    templates = Template.objects.filter(is_active=True)

    context = {
        'form': form,
        'formset': formset,
        'templates': templates,
        'is_new': is_new,
    }
    
    return render(request, 'core/card_builder.html', context)

@login_required
def card_success_view(request, card_id):
    """Success page after card creation"""
    user_card = get_object_or_404(UserCard.objects.prefetch_related("skills"), id=card_id, user=request.user)
    card_url = user_card.get_card_url()

    context = {
        'user_card': user_card,
        'card_url': card_url,
    }
    
    return render(request, 'core/card_success.html', context)

def view_card(request, username):
    """Public view to display user's digital card"""
    user_card = get_object_or_404(UserCard.objects.prefetch_related("skills"), username=username, is_published=True)
    user_card.views += 1
    user_card.save()

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

def pricing_view(request):
    plans = list(Plan.objects.select_related("discount").prefetch_related("Features").all())
    return render(request, 'core/pricing.html', context={'plans': plans})

def payment_success_view(request):
    return render(request, 'core/payment-success.html')

def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')
