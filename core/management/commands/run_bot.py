from django.core.management.base import BaseCommand
from bot.bot import run_bot

class Command(BaseCommand):
    help = 'Runs the Telegram bot for site management and backups'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot...'))
        run_bot()
