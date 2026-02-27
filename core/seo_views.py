from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import cache_page

from cards.models import UserCard


def _base_url(request):
    scheme = "https" if request.is_secure() else "http"
    return f"{scheme}://{request.get_host()}"


@cache_page(60 * 60)
def robots_txt_view(request):
    base_url = _base_url(request)
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Disallow: /login/",
        "Disallow: /signup/",
        "Disallow: /logout/",
        f"Sitemap: {base_url}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


@cache_page(60 * 30)
def sitemap_xml_view(request):
    base_url = _base_url(request)
    today = timezone.now().date().isoformat()

    static_urls = [
        (reverse("home"), today, "daily", "1.0"),
        (reverse("about"), today, "weekly", "0.8"),
        (reverse("buy_telegram"), today, "weekly", "0.7"),
        (reverse("card_builder"), today, "weekly", "0.8"),
    ]

    rows = []
    for path, lastmod, changefreq, priority in static_urls:
        rows.append(
            f"<url><loc>{base_url}{path}</loc><lastmod>{lastmod}</lastmod>"
            f"<changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>"
        )

    cards = UserCard.objects.filter(is_published=True).only("username", "updated_at")
    for card in cards.iterator():
        card_path = reverse("view_card", kwargs={"username": card.username})
        card_lastmod = card.updated_at.date().isoformat()
        rows.append(
            f"<url><loc>{base_url}{card_path}</loc><lastmod>{card_lastmod}</lastmod>"
            "<changefreq>weekly</changefreq><priority>0.6</priority></url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{''.join(rows)}"
        "</urlset>"
    )
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")

