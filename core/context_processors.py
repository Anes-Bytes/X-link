from django.core.cache import cache
from site_management.models import SiteContext, Banners


def site_context(request):
    data = cache.get("site_context_data")

    if data is None:
        context = SiteContext.objects.first()
        banners = list(Banners.objects.all())
        data = {
            "site_context": context,
            "banners": banners,
        }
        cache.set("site_context_data", data, 60 * 60)

    return data
