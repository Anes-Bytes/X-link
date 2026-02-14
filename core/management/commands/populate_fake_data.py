from django.core.management.base import BaseCommand
from site_management.models import SiteContext, Banners, Customer
from django.core.files.base import ContentFile
import base64

class Command(BaseCommand):
    help = 'Populates the database with high-quality Persian marketing content'

    def handle(self, *args, **options):
        self.stdout.write('Populating site data...')

        # Small 1x1 transparent GIF for placeholder
        placeholder_logo = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")

        # 1. Site Context
        site_context = SiteContext.objects.first()
        if not site_context:
            site_context = SiteContext.objects.create(
                site_name='ایکس‌لینک',
                hero_section_text_part1='کارت ویزیت هوشمند شما،',
                hero_section_text_part2='فراتر از یک تکه کاغذ!',
                hero_section_text_description='با ایکس‌لینک، در کمتر از ۵ دقیقه کارت ویزیت دیجیتال اختصاصی‌تان را طراحی کنید. تمام راه‌های ارتباطی، نمونه‌کارها و شبکه‌های اجتماعی خود را در یک لینک هوشمند به اشتراک بگذارید. حرفه‌ای دیده شوید و شبکه سازی خود را متحول کنید.',
                footer_section_text_part1='ایکس‌لینک؛ همراه همیشگی شما در دنیای ارتباطات دیجیتال.',
                footer_telegram_url='https://t.me/xlink_ir',
                footer_instagram_url='https://instagram.com/xlink.ir',
                footer_linkedin_url='https://linkedin.com/company/xlink-ir',
                footer_github_url='https://github.com/xlink-ir',
            )
            site_context.logo.save('logo.gif', ContentFile(placeholder_logo), save=True)
        else:
            site_context.site_name = 'ایکس‌لینک'
            site_context.hero_section_text_part1 = 'کارت ویزیت هوشمند شما،'
            site_context.hero_section_text_part2 = 'فراتر از یک تکه کاغذ!'
            site_context.hero_section_text_description = 'با ایکس‌لینک، در کمتر از ۵ دقیقه کارت ویزیت دیجیتال اختصاصی‌تان را طراحی کنید. تمام راه‌های ارتباطی، نمونه‌کارها و شبکه‌های اجتماعی خود را در یک لینک هوشمند به اشتراک بگذارید. حرفه‌ای دیده شوید و شبکه سازی خود را متحول کنید.'
            site_context.footer_section_text_part1 = 'ایکس‌لینک؛ همراه همیشگی شما در دنیای ارتباطات دیجیتال.'
            if not site_context.logo:
                site_context.logo.save('logo.gif', ContentFile(placeholder_logo), save=False)
            site_context.save()

        self.stdout.write(self.style.SUCCESS(f'SiteContext updated: {site_context.id}'))

        # 2. Banners
        Banners.objects.all().delete()
        
        banners_data = [
            {
                'title': 'طراحی سریع و حرفه‌ای',
                'description': 'در کمتر از ۵ دقیقه، هویت دیجیتال خود را بسازید و با دنیا به اشتراک بگذارید.'
            },
            {
                'title': 'مدیریت متمرکز لینک‌ها',
                'description': 'تمام شبکه‌های اجتماعی و راه‌های ارتباطی شما، فقط در یک لینک اختصاصی.'
            },
            {
                'title': 'آنالیز هوشمند بازدیدها',
                'description': 'ببینید چند نفر از کارت شما بازدید کرده‌اند و از کدام شهرها بوده‌اند.'
            }
        ]

        for item in banners_data:
            Banners.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('Banners populated.'))

        # 3. Customers
        Customer.objects.filter(site_context=site_context).delete()
        
        customers_data = [
            {'company_name': 'تپسی', 'company_url': 'https://tapsi.ir', 'display_order': 1},
            {'company_name': 'اسنپ', 'company_url': 'https://snapp.ir', 'display_order': 2},
            {'company_name': 'دیجی‌کالا', 'company_url': 'https://digikala.com', 'display_order': 3},
            {'company_name': 'دیوار', 'company_url': 'https://divar.ir', 'display_order': 4},
        ]

        for item in customers_data:
            Customer.objects.create(site_context=site_context, **item)

        self.stdout.write(self.style.SUCCESS('Customers populated.'))
        self.stdout.write(self.style.SUCCESS('Data population complete!'))
