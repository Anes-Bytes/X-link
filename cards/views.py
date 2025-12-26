import json
import logging

# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F

# Third-party imports
from environs import Env

# Local app imports
from core.models import UserPlan
from cards.models import *
from core.forms import UserCardForm, SkillInlineFormSet, ServiceInlineFormSet, PortfolioInlineFormSet

# Logger setup
logger = logging.getLogger(__name__)

# Env setup
env = Env()
env.read_env()

@login_required
def card_builder_view(request):
    user_card = (
        UserCard.objects
        .select_related('user')
        .prefetch_related(
            'skills',
            'services',
            'portfolio_items'
        )
        .filter(user=request.user)
        .first()
    )
    has_pro_plan = request.user.plan.filter(value=UserPlan.PlanChoices.Pro).exists()

    if request.method == 'POST':
        form = UserCardForm(request.POST, request.FILES, instance=user_card)
        skill_formset = SkillInlineFormSet(request.POST, instance=user_card, prefix='skill')
        service_formset = ServiceInlineFormSet(request.POST, instance=user_card, prefix='service')
        portfolio_formset = PortfolioInlineFormSet(request.POST, request.FILES, instance=user_card, prefix='portfolio')

        if (
            form.is_valid()
            and skill_formset.is_valid()
            and service_formset.is_valid()
            and portfolio_formset.is_valid()
        ):
            card = form.save(commit=False)
            card.user = request.user


            if has_pro_plan:
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

            logger.info(
                "Card saved for user %s, card_id=%s",
                request.user.username,
                card.id
            )
            return redirect('card_success', card_id=card.id)
        else:
            logger.warning(
                "Card form validation failed for user %s",
                request.user.username
            )
            logger.debug("Form errors: %s", form.errors)
            logger.debug("Skill errors: %s", skill_formset.errors)
            logger.debug("Service errors: %s", service_formset.errors)
            logger.debug("Portfolio errors: %s", portfolio_formset.errors)

    else:
        form = UserCardForm(instance=user_card)
        skill_formset = SkillInlineFormSet(instance=user_card, prefix='skill')
        service_formset = ServiceInlineFormSet(instance=user_card, prefix='service')
        portfolio_formset = PortfolioInlineFormSet(instance=user_card, prefix='portfolio')

    user_plans = request.user.plan.all()
    templates = Template.objects.prefetch_related("allowed_plans")

    for t in templates:
        # اگر allowed_plans خالی باشد یعنی همه می‌تونند استفاده کنند
        t.is_allowed = (
                not t.allowed_plans.exists() or
                t.allowed_plans.filter(id__in=user_plans).exists()
        )

    context = {
        'form': form,
        'skill_formset': skill_formset,
        'service_formset': service_formset,
        'portfolio_formset': portfolio_formset,
        'templates': templates,
        'has_pro_plan':has_pro_plan
    }

    return render(request, 'cards/card_builder.html', context)

@login_required
def card_success_view(request, card_id):
    user_card = get_object_or_404(
        UserCard.objects.prefetch_related("skills", "services", "portfolio_items"),
        id=card_id,
        user=request.user
    )
    card_url = user_card.get_card_url()

    logger.info("Card success page viewed by user %s for card_id=%s", request.user.username, card_id)
    messages.success(request, "کارت ویزیت شما با موفقیت ساخته شد")
    return render(request, 'cards/card_success.html', {
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

    return render(request, 'cards/card_view.html', context)


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
