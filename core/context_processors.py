from django.core.cache import cache
from types import SimpleNamespace

from site_management.models import SiteContext, Banners


def site_context(request):
    data = cache.get("site_context_data")

    if data is None:
        context = SiteContext.objects.first()
        if context is None:
            # Fallback values for fresh environments (e.g. local SQLite debug)
            context = SimpleNamespace(
                site_name="X-Link",
                logo=SimpleNamespace(url="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230a0f1f'/%3E%3Cpath d='M16 18h10l6 9 6-9h10L37 33l11 13H38l-6-9-6 9H16l11-13-11-15z' fill='%2300F6FF'/%3E%3C/svg%3E"),
                hero_section_text_part1="ساخت سایت و کارت ویزیت",
                hero_section_text_part2="با ایکس لینک",
                hero_section_text_description="در چند ثانیه صفحه حرفه‌ای خودت را بساز و منتشر کن.",
                footer_section_text_part1="X-Link",
                footer_telegram_url="https://t.me/AnesPy",
                footer_linkedin_url="",
                footer_github_url="",
                footer_instagram_url="",
                footer_enamad_badge="",
            )
        banners = list(Banners.objects.all())
        data = {
            "site_context": context,
            "banners": banners,
        }
        cache.set("site_context_data", data, 60 * 60)

    return data
