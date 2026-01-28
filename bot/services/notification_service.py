from aiogram import Bot
from datetime import datetime
from bot.database.models import BotSetting
from bot.config import ADMIN_CHANNEL_ID

class NotificationService:
    @staticmethod
    async def send_notification(bot: Bot, message: str, channel_id: int = None):
        if not channel_id:
            channel_id = await BotSetting.get_val("admin_channel_id", ADMIN_CHANNEL_ID)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"🔔 **اعلان سیستم**\n\n{message}\n\n🕒 زمان: `{timestamp}`"
        
        try:
            await bot.send_message(chat_id=channel_id, text=formatted_message, parse_mode="Markdown")
        except Exception as e:
            # Log error
            print(f"Error sending notification: {e}")

    @classmethod
    async def notify_user_login(cls, bot: Bot, username: str):
        await cls.send_notification(bot, f"👤 کاربر `{username}` وارد سیستم شد.")

    @classmethod
    async def notify_user_signup(cls, bot: Bot, username: str):
        await cls.send_notification(bot, f"🆕 کاربر جدید ثبت‌نام کرد: `{username}`")

    @classmethod
    async def notify_object_creation(cls, bot: Bot, obj_name: str, creator: str):
        await cls.send_notification(bot, f"🏗 `{obj_name}` توسط `{creator}` ایجاد شد.")
