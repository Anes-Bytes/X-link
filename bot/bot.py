import asyncio
import logging
from aiogram import Bot, Dispatcher
from tortoise import Tortoise

from bot.config import BOT_TOKEN, DATABASE_CONFIG
from bot.handlers import common, admin, backup, monitor
from bot.scheduler.main import setup_scheduler

async def main():
    # Logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/bot.log"),
            logging.StreamHandler()
        ]
    )

    # Database initialization
    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()

    # Bot initialization
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Register routers
    dp.include_router(common.router)
    dp.include_router(admin.router)
    dp.include_router(backup.router)
    dp.include_router(monitor.router)

    # Scheduler setup
    scheduler = setup_scheduler(bot)
    scheduler.start()

    # Start polling
    logging.info("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await Tortoise.close_connections()

def run_bot():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    run_bot()
