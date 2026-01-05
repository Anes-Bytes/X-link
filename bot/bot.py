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
        ['🏠 مدیریت سایت'],
        ['👥 مدیریت ادمین ها'],
        ['💾 بکاپ و سرور']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 خوش آمدید به ربات مدیریت X-link\n\nلطفاً یک دسته را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    text = update.message.text

    # Main Categories
    if text == '🏠 مدیریت سایت':
        keyboard = [
            ['📊 آمار سایت', '🌐 پنل مدیریت'],
            ['🔙 بازگشت به منو اصلی']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🏠 **مدیریت سایت**\n\nلطفاً یک گزینه را انتخاب کنید:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    elif text == '👥 مدیریت ادمین ها':
        keyboard = [
            ['➕ افزودن ادمین', '➖ حذف ادمین'],
            ['👥 لیست ادمین ها'],
            ['🔙 بازگشت به منو اصلی']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "👥 **مدیریت ادمین ها**\n\nلطفاً یک گزینه را انتخاب کنید:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    elif text == '💾 بکاپ و سرور':
        keyboard = [
            ['📦 بکاپ فوری', '🖥 وضعیت سرور'],
            ['🔙 بازگشت به منو اصلی']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "💾 **بکاپ و سرور**\n\nلطفاً یک گزینه را انتخاب کنید:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    # Site Management Options
    elif text == '📊 آمار سایت':
        try:
            stats = get_site_stats()
            msg = (
                "📊 **آمار سایت X-link**\n\n"
                f"👤 تعداد کاربران: {stats['users_count']}\n"
                f"🪪 تعداد کارت‌ها: {stats['cards_count']}\n"
            )
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در دریافت آمار سایت: {str(e)}")

    elif text == '🌐 پنل مدیریت':
        keyboard = [[InlineKeyboardButton("ورود به پنل", url="https://x-link.ir/Xdash/")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("برای ورود به پنل مدیریت روی دکمه زیر کلیک کنید:", reply_markup=reply_markup)

    # Admin Management Options
    elif text == '➕ افزودن ادمین':
        await update.message.reply_text("لطفاً ID عددی کاربر را با فرمت `/add_admin ID` ارسال کنید.")

    elif text == '➖ حذف ادمین':
        await update.message.reply_text("لطفاً ID عددی ادمین را با فرمت `/remove_admin ID` ارسال کنید.")

    elif text == '👥 لیست ادمین ها':
        try:
            admins = db.get_all_admins()
            if admins:
                admin_list = "\n".join([f"• `{admin_id}`" for admin_id in admins])
                msg = f"👥 **لیست ادمین های ربات**\n\n{admin_list}"
            else:
                msg = "👥 هیچ ادمینی یافت نشد."
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در دریافت لیست ادمین‌ها: {str(e)}")

    # Backup and Server Options
    elif text == '🖥 وضعیت سرور':
        try:
            stats = get_system_stats()
            msg = (
                "🖥 **وضعیت سرور**\n\n"
                f"🔥 مصرف CPU: {stats['cpu']}%\n"
                f"🧠 مصرف RAM: {stats['ram_percent']}% ({stats['ram_used']}GB / {stats['ram_total']}GB)\n"
                f"💾 فضای دیسک: {stats['disk_percent']}% ({stats['disk_used']}GB / {stats['disk_total']}GB)\n"
                f"📶 پینگ: {stats['ping']}ms"
            )
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در دریافت وضعیت سرور: {str(e)}")

    elif text == '📦 بکاپ فوری':
        await update.message.reply_text("⏳ در حال تهیه بکاپ...")
        try:
            path, filename = create_backup()
            await update.message.reply_document(
                document=open(path, 'rb'),
                filename=filename,
                caption="✅ بکاپ با موفقیت تهیه شد.\n\nشامل:\n• دیتابیس SQLite\n• دیتابیس MySQL\n• فایل‌های مدیا"
            )
            db.log_backup(filename, "Success")
            await notify_admins(context.bot, f"✅ بکاپ خودکار با موفقیت انجام شد: {filename}")
        except Exception as e:
            error_msg = f"❌ خطا در تهیه بکاپ: {str(e)}"
            await update.message.reply_text(error_msg)
            db.log_backup("N/A", f"Failed: {str(e)}")
            await notify_admins(context.bot, f"❌ خطای بکاپ: {str(e)}")

    # Navigation
    elif text == '🔙 بازگشت به منو اصلی':
        keyboard = [
            ['🏠 مدیریت سایت'],
            ['👥 مدیریت ادمین ها'],
            ['💾 بکاپ و سرور']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🏠 بازگشت به منو اصلی\n\nلطفاً یک دسته را انتخاب کنید:",
            reply_markup=reply_markup
        )

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
            await notify_admins(context.bot, f"👤 ادمین جدید اضافه شد: {new_admin_id}")
        else:
            await update.message.reply_text("❌ خطا در افزودن ادمین.")
    else:
        await update.message.reply_text("❌ ID نامعتبر است.")

async def remove_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    if not context.args:
        await update.message.reply_text("لطفاً ID عددی ادمین را وارد کنید. مثال: `/remove_admin 12345678`")
        return

    admin_id_to_remove = context.args[0]
    if admin_id_to_remove.isdigit():
        admin_id_int = int(admin_id_to_remove)
        # Prevent removing yourself
        if admin_id_int == user_id:
            await update.message.reply_text("❌ نمی‌توانید خودتان را از لیست ادمین‌ها حذف کنید.")
            return

        if db.remove_admin(admin_id_int):
            await update.message.reply_text(f"✅ ادمین {admin_id_to_remove} با موفقیت حذف شد.")
            await notify_admins(context.bot, f"👤 ادمین حذف شد: {admin_id_to_remove}")
        else:
            await update.message.reply_text("❌ خطا در حذف ادمین یا ادمین یافت نشد.")
    else:
        await update.message.reply_text("❌ ID نامعتبر است.")

async def hourly_backup(context: ContextTypes.DEFAULT_TYPE):
    logger.info("Starting hourly backup...")
    try:
        path, filename = create_backup()

        # Priority: Channel > Admins
        target_id = getattr(settings, 'TELEGRAM_BACKUP_CHANNEL_ID', None)
        success_sent = False

        if target_id:
            try:
                await context.bot.send_document(
                    chat_id=target_id,
                    document=open(path, 'rb'),
                    filename=filename,
                    caption=f"📦 بکاپ خودکار یک ساعته\n⏰ {datetime.now().strftime('%H:%M:%S')}\n\n✅ شامل دیتابیس‌ها و فایل‌های مدیا"
                )
                success_sent = True
            except Exception as e:
                logger.error(f"Failed to send backup to channel {target_id}: {e}")
                await notify_admins(context.bot, f"❌ خطا در ارسال بکاپ به کانال: {e}")

        if not success_sent:
            # Fallback to admins if no channel configured or channel failed
            admins = db.get_all_admins()
            for admin_id in admins:
                try:
                    await context.bot.send_document(
                        chat_id=admin_id,
                        document=open(path, 'rb'),
                        filename=filename,
                        caption=f"📦 بکاپ خودکار یک ساعته\n⏰ {datetime.now().strftime('%H:%M:%S')}\n\n✅ شامل دیتابیس‌ها و فایل‌های مدیا"
                    )
                    success_sent = True
                except Exception as e:
                    logger.error(f"Failed to send backup to {admin_id}: {e}")

        if success_sent:
            db.log_backup(filename, "Success")
            await notify_admins(context.bot, f"✅ بکاپ خودکار یک ساعته با موفقیت انجام شد: {filename}")
        else:
            db.log_backup(filename, "Failed: Could not send to any destination")
            await notify_admins(context.bot, f"❌ بکاپ تهیه شد اما ارسال نشد: {filename}")

    except Exception as e:
        logger.error(f"Hourly backup failed: {e}")
        db.log_backup("N/A", f"Failed: {e}")
        await notify_admins(context.bot, f"❌ خطای کلی در بکاپ خودکار: {e}")

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
    application.add_handler(CommandHandler("remove_admin", remove_admin_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Job Queue for hourly backup
    job_queue = application.job_queue
    job_queue.run_repeating(hourly_backup, interval=3600, first=10)

    logger.info("Bot started...")
    application.run_polling()

if __name__ == '__main__':
    run_bot()
