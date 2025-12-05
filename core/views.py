from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import UserCard, Skill
from .forms import UserCardForm, SkillInlineFormSet
from Xlink.models import CardTemplate


def card_builder_view(request):
    """Main card builder view - handles card creation and editing"""
    try:
        user_card = UserCard.objects.get(user=request.user)
        is_new = False
    except UserCard.DoesNotExist:
        user_card = UserCard(user=request.user)
        is_new = True

    if request.method == 'POST':
        form = UserCardForm(request.POST, instance=user_card)
        formset = SkillInlineFormSet(request.POST, instance=user_card)

        if form.is_valid() and formset.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            
            formset.instance = card
            formset.save()

            # Redirect to success page
            return redirect('card_success', card_id=card.id)
    else:
        form = UserCardForm(instance=user_card)
        formset = SkillInlineFormSet(instance=user_card) if not is_new else SkillInlineFormSet()

    templates = CardTemplate.objects.filter(is_active=True)
    
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
    user_card = get_object_or_404(UserCard, id=card_id, user=request.user)
    card_url = user_card.get_card_url()
    
    context = {
        'user_card': user_card,
        'card_url': card_url,
    }
    
    return render(request, 'core/card_success.html', context)


def view_card(request, username):
    """Public view to display user's digital card"""
    user_card = get_object_or_404(UserCard, username=username, is_published=True)
    
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
def publish_card(request, card_id):
    """Publish or unpublish a user card"""
    user_card = get_object_or_404(UserCard, id=card_id, user=request.user)
    user_card.is_published = not user_card.is_published
    user_card.save()
    
    return JsonResponse({
        'success': True,
        'is_published': user_card.is_published,
    })
