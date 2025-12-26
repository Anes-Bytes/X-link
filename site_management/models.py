from django.db import models

class SiteContext(models.Model):
    site_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logo')
    hero_section_text_part1 = models.CharField(max_length=200)
    hero_section_text_part2 = models.CharField(max_length=200)
    hero_section_text_description = models.CharField(max_length=200)

    footer_section_text_part1 = models.CharField(max_length=200)
    footer_telegram_url = models.URLField(null=True, blank=True)
    footer_linkedin_url = models.URLField(null=True, blank=True)
    footer_github_url = models.URLField(null=True, blank=True)
    footer_instagram_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.site_name


class Banners(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners', blank=True)

    def __str__(self):
        return self.title


class Customers(models.Model):
    SiteContext = models.ForeignKey('SiteContext', on_delete=models.CASCADE, related_name='Customers')
    company_name = models.CharField(max_length=200)
    company_url = models.URLField()
    company_logo = models.ImageField(upload_to='company_logo')

    def __str__(self):
        return self.company_name
