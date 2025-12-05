from .models import SiteContext, UserCard, Skill


def site_context(request):
    context = SiteContext.objects.first()
    
    # Add user card if user is authenticated
    user_card = None
    skills = []
    if request.user.is_authenticated:
        user_card = UserCard.objects.filter(user=request.user).first()
        if user_card:
            skills = user_card.skills.all()
    
    return {
        "site_context": context,
        "user_card": user_card,
        "skills": skills,
    }
