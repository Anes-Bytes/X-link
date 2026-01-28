from bot.database.models import Admin, BotSetting
from bot.config import OWNER_ID

class AdminService:
    @staticmethod
    async def is_admin(telegram_id: int) -> bool:
        if telegram_id == OWNER_ID:
            return True
        return await Admin.filter(telegram_id=telegram_id).exists()

    @staticmethod
    async def add_admin(telegram_id: int, username: str = None):
        await Admin.get_or_create(telegram_id=telegram_id, defaults={"username": username})

    @staticmethod
    async def remove_admin(telegram_id: int):
        await Admin.filter(telegram_id=telegram_id).delete()

    @staticmethod
    async def get_all_admins():
        return await Admin.all()
