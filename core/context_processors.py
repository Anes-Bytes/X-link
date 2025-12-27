from django.core.cache import cache
from site_management.models import SiteContext, Banners


def site_context(request):
    context = cache.get("site_context")
    banners = cache.get("banners")

    if context is None:
        context = SiteContext.objects.first()
        cache.set("site_context", context, 60 * 60)
    if banners is None:
        banners = Banners.objects.all()
        cache.set("banners", banners, 60 * 60)

    return {
        "site_context": context,
        "banners": banners,
    }
