import requests
import logging
from django.conf import settings
from bot.database import BotDatabase

logger = logging.getLogger(__name__)

def send_telegram_notification(message):
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found for notification")
        return

    db = BotDatabase()
    admins = db.get_all_admins()
    
    for admin_id in admins:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": admin_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, json=payload)
            if not response.ok:
                logger.error(f"Failed to send telegram notification: {response.text}")
        except Exception as e:
            logger.error(f"Error sending telegram notification: {e}")
