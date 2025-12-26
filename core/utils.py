import logging
from melipayamak import Api
from environs import Env
# Logger setup
logger = logging.getLogger(__name__)

# Env setup
env = Env()
env.read_env()


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


