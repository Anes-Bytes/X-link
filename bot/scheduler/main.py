import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types
from bot.services.backup_service import BackupService
from bot.database.models import BotSetting
from bot.config import BACKUP_CHANNEL_ID

async def scheduled_backup(bot: Bot):
    try:
        zip_path = await BackupService.create_backup()
        channel_id = await BotSetting.get_val("backup_channel_id", BACKUP_CHANNEL_ID)
        
        document = types.FSInputFile(zip_path)
        await bot.send_document(
            chat_id=channel_id,
            document=document,
            caption=f"📦 نسخه پشتیبان خودکار\n📅 تاریخ: {os.path.basename(zip_path)}"
        )
        
        if os.path.exists(zip_path):
            os.remove(zip_path)
    except Exception as e:
        print(f"Error in scheduled backup: {e}")

def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    # Default interval: 60 minutes
    scheduler.add_job(scheduled_backup, "interval", minutes=60, args=[bot], id="backup_job")
    return scheduler

async def update_scheduler_interval(scheduler: AsyncIOScheduler, minutes: int):
    scheduler.reschedule_job("backup_job", trigger="interval", minutes=minutes)
