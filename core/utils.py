import logging
from melipayamak import Api
from environs import Env
# Logger setup
logger = logging.getLogger(__name__)

# Env setup
env = Env()
env.read_env()


import requests
from datetime import datetime

def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    return ip


def send_telegram_notification(message: str):
    """
    Send notification to Telegram admin channel
    """
    token = env("TELEGRAM_BOT_TOKEN")
    chat_id = env("TELEGRAM_ADMIN_CHAT_IDS")
    
    if not token or not chat_id:
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"🔔 **اعلان سیستم**\n\n{message}\n\n🕒 زمان: `{timestamp}`"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": chat_id,
            "text": formatted_message,
            "parse_mode": "Markdown"
        }, timeout=5)
    except Exception as e:
        logger.error("Telegram notification failed: %s", e)


def send_sms(phone: str, content: str) -> bool:
    """
    Send OTP SMS via Melipayamak
    """
    try:
        username = env("MELIPAYAMAK_USERNAME")
        password = env("MELIPAYAMAK_APIKEY")
        sender = env("MELIPAYAMAK_NUMBER")

        api = Api(username, password)
        sms = api.sms()


        sms.send(phone, sender, content)
        return True

    except Exception as e:
        logger.error("SMS send failed for %s: %s", phone, e)
        return False


