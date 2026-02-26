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
                site_name='Ø§ÛŒÚ©Ø³â€ŒÙ„ÛŒÙ†Ú©',
                hero_section_text_part1='Ú©Ø§Ø±Øª ÙˆÛŒØ²ÛŒØª Ù‡ÙˆØ´Ù…Ù†Ø¯ Ø´Ù…Ø§ØŒ',
                hero_section_text_part2='ÙØ±Ø§ØªØ± Ø§Ø² ÛŒÚ© ØªÚ©Ù‡ Ú©Ø§ØºØ°!',
                hero_section_text_description='Ø¨Ø§ Ø§ÛŒÚ©Ø³â€ŒÙ„ÛŒÙ†Ú©ØŒ Ø¯Ø± Ú©Ù…ØªØ± Ø§Ø² Ûµ Ø¯Ù‚ÛŒÙ‚Ù‡ Ú©Ø§Ø±Øª ÙˆÛŒØ²ÛŒØª Ø¯ÛŒØ¬ÛŒØªØ§Ù„ Ø§Ø®ØªØµØ§ØµÛŒâ€ŒØªØ§Ù† Ø±Ø§ Ø·Ø±Ø§Ø­ÛŒ Ú©Ù†ÛŒØ¯. ØªÙ…Ø§Ù… Ø±Ø§Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ø±ØªØ¨Ø§Ø·ÛŒØŒ Ù†Ù…ÙˆÙ†Ù‡â€ŒÚ©Ø§Ø±Ù‡Ø§ Ùˆ Ø´Ø¨Ú©Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ø¬ØªÙ…Ø§Ø¹ÛŒ Ø®ÙˆØ¯ Ø±Ø§ Ø¯Ø± ÛŒÚ© Ù„ÛŒÙ†Ú© Ù‡ÙˆØ´Ù…Ù†Ø¯ Ø¨Ù‡ Ø§Ø´ØªØ±Ø§Ú© Ø¨Ú¯Ø°Ø§Ø±ÛŒØ¯. Ø­Ø±ÙÙ‡â€ŒØ§ÛŒ Ø¯ÛŒØ¯Ù‡ Ø´ÙˆÛŒØ¯ Ùˆ Ø´Ø¨Ú©Ù‡ Ø³Ø§Ø²ÛŒ Ø®ÙˆØ¯ Ø±Ø§ Ù…ØªØ­ÙˆÙ„ Ú©Ù†ÛŒØ¯.',
                footer_section_text_part1='Ø§ÛŒÚ©Ø³â€ŒÙ„ÛŒÙ†Ú©Ø› Ù‡Ù…Ø±Ø§Ù‡ Ù‡Ù…ÛŒØ´Ú¯ÛŒ Ø´Ù…Ø§ Ø¯Ø± Ø¯Ù†ÛŒØ§ÛŒ Ø§Ø±ØªØ¨Ø§Ø·Ø§Øª Ø¯ÛŒØ¬ÛŒØªØ§Ù„.',
                footer_telegram_url='https://t.me/xlink_ir',
                footer_instagram_url='https://instagram.com/xlink.ir',
                footer_linkedin_url='https://linkedin.com/company/xlink-ir',
                footer_github_url='https://github.com/xlink-ir',
            )
            site_context.logo.save('logo.gif', ContentFile(placeholder_logo), save=True)
        else:
            site_context.site_name = 'Ø§ÛŒÚ©Ø³â€ŒÙ„ÛŒÙ†Ú©'
            site_context.hero_section_text_part1 = 'Ú©Ø§Ø±Øª ÙˆÛŒØ²ÛŒØª Ù‡ÙˆØ´Ù…Ù†Ø¯ Ø´Ù…Ø§ØŒ'
            site_context.hero_section_text_part2 = 'ÙØ±Ø§ØªØ± Ø§Ø² ÛŒÚ© ØªÚ©Ù‡ Ú©Ø§ØºØ°!'
            site_context.hero_section_text_description = 'Ø¨Ø§ Ø§ÛŒÚ©Ø³â€ŒÙ„ÛŒÙ†Ú©ØŒ Ø¯Ø± Ú©Ù…ØªØ± Ø§Ø² Ûµ Ø¯Ù‚ÛŒÙ‚Ù‡ Ú©Ø§Ø±Øª ÙˆÛŒØ²ÛŒØª Ø¯ÛŒØ¬ÛŒØªØ§Ù„ Ø§Ø®ØªØµØ§ØµÛŒâ€ŒØªØ§Ù† Ø±Ø§ Ø·Ø±Ø§Ø­ÛŒ Ú©Ù†ÛŒØ¯. ØªÙ…Ø§Ù… Ø±Ø§Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ø±ØªØ¨Ø§Ø·ÛŒØŒ Ù†Ù…ÙˆÙ†Ù‡â€ŒÚ©Ø§Ø±Ù‡Ø§ Ùˆ Ø´Ø¨Ú©Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ø¬ØªÙ…Ø§Ø¹ÛŒ Ø®ÙˆØ¯ Ø±Ø§ Ø¯Ø± ÛŒÚ© Ù„ÛŒÙ†Ú© Ù‡ÙˆØ´Ù…Ù†Ø¯ Ø¨Ù‡ Ø§Ø´ØªØ±Ø§Ú© Ø¨Ú¯Ø°Ø§Ø±ÛŒØ¯. Ø­Ø±ÙÙ‡â€ŒØ§ÛŒ Ø¯ÛŒØ¯Ù‡ Ø´ÙˆÛŒØ¯ Ùˆ Ø´Ø¨Ú©Ù‡ Ø³Ø§Ø²ÛŒ Ø®ÙˆØ¯ Ø±Ø§ Ù…ØªØ­ÙˆÙ„ Ú©Ù†ÛŒØ¯.'
            site_context.footer_section_text_part1 = 'Ø§ÛŒÚ©Ø³â€ŒÙ„ÛŒÙ†Ú©Ø› Ù‡Ù…Ø±Ø§Ù‡ Ù‡Ù…ÛŒØ´Ú¯ÛŒ Ø´Ù…Ø§ Ø¯Ø± Ø¯Ù†ÛŒØ§ÛŒ Ø§Ø±ØªØ¨Ø§Ø·Ø§Øª Ø¯ÛŒØ¬ÛŒØªØ§Ù„.'
            if not site_context.logo:
                site_context.logo.save('logo.gif', ContentFile(placeholder_logo), save=False)
            site_context.save()

        self.stdout.write(self.style.SUCCESS(f'SiteContext updated: {site_context.id}'))

        # 2. Banners
        Banners.objects.all().delete()
        
        banners_data = [
            {
                'title': 'Ø·Ø±Ø§Ø­ÛŒ Ø³Ø±ÛŒØ¹ Ùˆ Ø­Ø±ÙÙ‡â€ŒØ§ÛŒ',
                'description': 'Ø¯Ø± Ú©Ù…ØªØ± Ø§Ø² Ûµ Ø¯Ù‚ÛŒÙ‚Ù‡ØŒ Ù‡ÙˆÛŒØª Ø¯ÛŒØ¬ÛŒØªØ§Ù„ Ø®ÙˆØ¯ Ø±Ø§ Ø¨Ø³Ø§Ø²ÛŒØ¯ Ùˆ Ø¨Ø§ Ø¯Ù†ÛŒØ§ Ø¨Ù‡ Ø§Ø´ØªØ±Ø§Ú© Ø¨Ú¯Ø°Ø§Ø±ÛŒØ¯.'
            },
            {
                'title': 'Ù…Ø¯ÛŒØ±ÛŒØª Ù…ØªÙ…Ø±Ú©Ø² Ù„ÛŒÙ†Ú©â€ŒÙ‡Ø§',
                'description': 'ØªÙ…Ø§Ù… Ø´Ø¨Ú©Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ø¬ØªÙ…Ø§Ø¹ÛŒ Ùˆ Ø±Ø§Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ø±ØªØ¨Ø§Ø·ÛŒ Ø´Ù…Ø§ØŒ ÙÙ‚Ø· Ø¯Ø± ÛŒÚ© Ù„ÛŒÙ†Ú© Ø§Ø®ØªØµØ§ØµÛŒ.'
            },
            {
                'title': 'Ø¢Ù†Ø§Ù„ÛŒØ² Ù‡ÙˆØ´Ù…Ù†Ø¯ Ø¨Ø§Ø²Ø¯ÛŒØ¯Ù‡Ø§',
                'description': 'Ø¨Ø¨ÛŒÙ†ÛŒØ¯ Ú†Ù†Ø¯ Ù†ÙØ± Ø§Ø² Ú©Ø§Ø±Øª Ø´Ù…Ø§ Ø¨Ø§Ø²Ø¯ÛŒØ¯ Ú©Ø±Ø¯Ù‡â€ŒØ§Ù†Ø¯ Ùˆ Ø§Ø² Ú©Ø¯Ø§Ù… Ø´Ù‡Ø±Ù‡Ø§ Ø¨ÙˆØ¯Ù‡â€ŒØ§Ù†Ø¯.'
            }
        ]

        for item in banners_data:
            Banners.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('Banners populated.'))

        # 3. Customers
        Customer.objects.filter(site_context=site_context).delete()
        
        customers_data = [
            {'company_name': 'ØªÙ¾Ø³ÛŒ', 'company_url': 'https://tapsi.ir', 'display_order': 1, 'is_test': True},
            {'company_name': 'Ø§Ø³Ù†Ù¾', 'company_url': 'https://snapp.ir', 'display_order': 2, 'is_test': True},
            {'company_name': 'Ø¯ÛŒØ¬ÛŒâ€ŒÚ©Ø§Ù„Ø§', 'company_url': 'https://digikala.com', 'display_order': 3, 'is_test': True},
            {'company_name': 'Ø¯ÛŒÙˆØ§Ø±', 'company_url': 'https://divar.ir', 'display_order': 4, 'is_test': True},
        ]

        for item in customers_data:
            Customer.objects.create(site_context=site_context, **item)

        self.stdout.write(self.style.SUCCESS('Customers populated.'))
        self.stdout.write(self.style.SUCCESS('Data population complete!'))

