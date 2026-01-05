import os
import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from django.conf import settings
from bot.database import BotDatabase
from bot.utils import get_system_stats, create_backup, get_site_stats

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

db = BotDatabase()

# Add initial admins from settings
for admin_id in settings.TELEGRAM_ADMIN_CHAT_IDS:
    db.add_admin(int(admin_id))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text("❌ شما دسترسی به این ربات را ندارید.")
        return

    keyboard = [
        ['📊 آمار سایت', '🖥 وضعیت سرور'],
        ['🔐 افزودن ادمین', '🌐 پنل مدیریت'],
        ['📦 بکاپ فوری']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 خوش آمدید به ربات مدیریت X-link\nلطفاً یک گزینه را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    text = update.message.text

    if text == '📊 آمار سایت':
        stats = get_site_stats()
        msg = (
            "📊 **آمار سایت X-link**\n\n"
            f"👤 تعداد کاربران: {stats['users_count']}\n"
            f"🪪 تعداد کارت‌ها: {stats['cards_count']}\n"
            f"🛠 مهارت‌ها: {stats['skills_count']}\n"
            f"💼 سرویس‌ها: {stats['services_count']}\n"
            f"📁 نمونه کارها: {stats['portfolios_count']}"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    elif text == '🖥 وضعیت سرور':
        stats = get_system_stats()
        msg = (
            "🖥 **وضعیت سرور**\n\n"
            f"🔥 مصرف CPU: {stats['cpu']}%\n"
            f"🧠 مصرف RAM: {stats['ram_percent']}% ({stats['ram_used']}GB / {stats['ram_total']}GB)\n"
            f"💾 فضای دیسک: {stats['disk_percent']}% ({stats['disk_used']}GB / {stats['disk_total']}GB)\n"
            f"📶 پینگ: {stats['ping']}ms"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    elif text == '🔐 افزودن ادمین':
        await update.message.reply_text("لطفاً ID عددی کاربر را با فرمت `/add_admin ID` ارسال کنید.")

    elif text == '🌐 پنل مدیریت':
        keyboard = [[InlineKeyboardButton("ورود به پنل", url="https://x-link.ir/Xdash/")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("برای ورود به پنل مدیریت روی دکمه زیر کلیک کنید:", reply_markup=reply_markup)

    elif text == '📦 بکاپ فوری':
        await update.message.reply_text("⏳ در حال تهیه بکاپ...")
        try:
            path, filename = create_backup()
            await update.message.reply_document(document=open(path, 'rb'), filename=filename, caption="✅ بکاپ با موفقیت تهیه شد.")
            db.log_backup(filename, "Success")
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در تهیه بکاپ: {str(e)}")
            db.log_backup("N/A", f"Failed: {str(e)}")

async def add_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    if not context.args:
        await update.message.reply_text("لطفاً ID عددی را وارد کنید. مثال: `/add_admin 12345678`")
        return

    new_admin_id = context.args[0]
    if new_admin_id.isdigit():
        if db.add_admin(int(new_admin_id)):
            await update.message.reply_text(f"✅ کاربر {new_admin_id} با موفقیت به ادمین‌ها اضافه شد.")
        else:
            await update.message.reply_text("❌ خطا در افزودن ادمین.")
    else:
        await update.message.reply_text("❌ ID نامعتبر است.")

async def hourly_backup(context: ContextTypes.DEFAULT_TYPE):
    logger.info("Starting hourly backup...")
    try:
        path, filename = create_backup()
        
        # Priority: Channel > Admins
        target_id = getattr(settings, 'TELEGRAM_BACKUP_CHANNEL_ID', None)
        
        if target_id:
            try:
                await context.bot.send_document(
                    chat_id=target_id,
                    document=open(path, 'rb'),
                    filename=filename,
                    caption=f"📦 بکاپ خودکار یک ساعته\n⏰ {datetime.now().strftime('%H:%M:%S')}"
                )
            except Exception as e:
                logger.error(f"Failed to send backup to channel {target_id}: {e}")
        else:
            # Fallback to admins if no channel configured
            admins = db.get_all_admins()
            for admin_id in admins:
                try:
                    await context.bot.send_document(
                        chat_id=admin_id,
                        document=open(path, 'rb'),
                        filename=filename,
                        caption=f"📦 بکاپ خودکار یک ساعته\n⏰ {datetime.now().strftime('%H:%M:%S')}"
                    )
                except Exception as e:
                    logger.error(f"Failed to send backup to {admin_id}: {e}")
        
        db.log_backup(filename, "Success")
    except Exception as e:
        logger.error(f"Hourly backup failed: {e}")
        db.log_backup("N/A", f"Failed: {e}")

async def notify_admins(bot, message):
    admins = db.get_all_admins()
    for admin_id in admins:
        try:
            await bot.send_message(chat_id=admin_id, text=message)
        except Exception as e:
            logger.error(f"Failed to notify {admin_id}: {e}")

def run_bot():
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in settings!")
        return

    application = ApplicationBuilder().token(token).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_admin", add_admin_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Job Queue for hourly backup
    job_queue = application.job_queue
    job_queue.run_repeating(hourly_backup, interval=3600, first=10)

    logger.info("Bot started...")
    application.run_polling()

if __name__ == '__main__':
    run_bot()
