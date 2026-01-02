"""
Django management command to run the Telegram bot for server monitoring and backup management.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Optional

import schedule
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.utils import timezone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from core.models import TelegramBot
from core.server_utils import (
    get_server_resources,
    format_server_resources_markdown,
    create_database_backup,
    format_backup_result_markdown,
    cleanup_old_backups
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/telegram_bot.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)


class TelegramBotHandler:
    """
    Main handler class for Telegram bot operations.
    """

    def __init__(self, bot_config: TelegramBot):
        self.bot_config = bot_config
        self.application: Optional[Application] = None

    async def get_bot_config_async(self) -> TelegramBot:
        """Get fresh bot config from database asynchronously."""
        return await sync_to_async(TelegramBot.objects.get)(pk=self.bot_config.pk)

    @sync_to_async
    def update_bot_config(self, **kwargs) -> None:
        """Update bot config in database synchronously."""
        TelegramBot.objects.filter(pk=self.bot_config.pk).update(**kwargs)
        self.bot_config.refresh_from_db()

    async def is_admin_async(self, chat_id: int) -> bool:
        """Check admin access asynchronously."""
        config = await self.get_bot_config_async()
        return config.is_admin(chat_id)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command."""
        try:
            if not update.effective_chat:
                return

            chat_id = update.effective_chat.id
            logger.info(f"Start command from chat_id: {chat_id}")

            # Create inline keyboard
            keyboard = [
                [
                    InlineKeyboardButton("📊 Ping & Resources", callback_data="ping_resources"),
                    InlineKeyboardButton("💾 Manual Backup", callback_data="manual_backup")
                ],
                [
                    InlineKeyboardButton("❓ Help", callback_data="help")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            welcome_text = (
                "🤖 *X-Link Server Monitor Bot*\n\n"
                "Welcome! I'm your server monitoring assistant.\n\n"
                "Choose an option from the menu below:"
            )

            await update.message.reply_text(
                welcome_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )

        except Exception as e:
            logger.error(f"Error in start_command: {e}")
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ Sorry, an error occurred. Please try again."
                )

    async def ping_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /ping command."""
        try:
            if not update.effective_chat:
                return

            chat_id = update.effective_chat.id
            logger.info(f"Ping command from chat_id: {chat_id}")

            # Get server resources
            resources_text = await self.get_server_resources_async()

            await update.message.reply_text(
                f"📊 *Server Resources:*\n\n{resources_text}",
                parse_mode='Markdown'
            )

        except Exception as e:
            logger.error(f"Error in ping_command: {e}")
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ Error getting server resources."
                )

    async def backup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /backup command (admin only)."""
        try:
            if not update.effective_chat:
                return

            chat_id = update.effective_chat.id
            logger.info(f"Backup command from chat_id: {chat_id}")

            # Check admin access
            if not await self.is_admin_async(chat_id):
                await update.message.reply_text("❌ Access denied. Admin privileges required.")
                return

            # Start backup process
            status_message = await update.message.reply_text("🔄 Starting database backup...")

            try:
                backup_result = await self.create_backup_async()
                await status_message.edit_text(backup_result)
            except Exception as e:
                logger.error(f"Backup failed: {e}")
                await status_message.edit_text(f"❌ Backup failed: {str(e)}")

        except Exception as e:
            logger.error(f"Error in backup_command: {e}")
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ An error occurred during backup."
                )

    async def callback_query_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle inline keyboard button presses."""
        try:
            query = update.callback_query
            if not query or not query.data:
                return

            await query.answer()

            chat_id = query.message.chat_id
            logger.info(f"Callback query: {query.data} from chat_id: {chat_id}")

            if query.data == "ping_resources":
                resources_text = await self.get_server_resources_async()
                await query.edit_message_text(
                    f"📊 *Server Resources:*\n\n{resources_text}",
                    parse_mode='Markdown'
                )

            elif query.data == "manual_backup":
                # Check admin access
                if not await self.is_admin_async(chat_id):
                    await query.edit_message_text("❌ Access denied. Admin privileges required.")
                    return

                # Start backup process
                await query.edit_message_text("🔄 Starting database backup...")
                try:
                    backup_result = await self.create_backup_async()
                    await query.edit_message_text(backup_result)
                except Exception as e:
                    logger.error(f"Backup failed: {e}")
                    await query.edit_message_text(f"❌ Backup failed: {str(e)}")

            elif query.data == "help":
                help_text = (
                    "🤖 *X-Link Server Monitor Bot Help*\n\n"
                    "*Commands:*\n"
                    "/start - Show main menu\n"
                    "/ping - Show server resources\n"
                    "/backup - Create database backup (admin only)\n\n"
                    "*Features:*\n"
                    "• Real-time server monitoring (CPU, RAM, Disk)\n"
                    "• Manual database backups\n"
                    "• Scheduled automatic backups\n"
                    "• Admin-only backup controls\n\n"
                    "*Admin Features:*\n"
                    "• Manual backup creation\n"
                    "• Automatic scheduled backups\n"
                    "• Backup file delivery via Telegram"
                )
                await query.edit_message_text(help_text, parse_mode='Markdown')

        except Exception as e:
            logger.error(f"Error in callback_query_handler: {e}")
            try:
                await query.edit_message_text("❌ An error occurred. Please try again.")
            except:
                pass

    async def get_server_resources_async(self) -> str:
        """Get server resources asynchronously."""
        return await sync_to_async(format_server_resources_markdown)(
            await sync_to_async(get_server_resources)()
        )

    async def create_backup_async(self) -> str:
        """Create database backup asynchronously."""
        # Create backup
        backup_result = await sync_to_async(create_database_backup)()

        if backup_result['success']:
            # Update last backup time
            await self.update_bot_config(last_backup_at=timezone.now())

            # Return formatted result
            return format_backup_result_markdown(backup_result)
        else:
            raise Exception(backup_result.get('error', 'Unknown backup error'))

    async def send_backup_to_admins(self, backup_path: str, filename: str) -> None:
        """Send backup file to all admin users."""
        if not self.application:
            return

        try:
            config = await self.get_bot_config_async()

            for admin_id in config.admin_chat_ids:
                try:
                    with open(backup_path, 'rb') as backup_file:
                        await self.application.bot.send_document(
                            chat_id=admin_id,
                            document=backup_file,
                            filename=filename,
                            caption=f"🔄 Scheduled database backup\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        )
                    logger.info(f"Backup sent to admin {admin_id}")
                except Exception as e:
                    logger.error(f"Failed to send backup to admin {admin_id}: {e}")

        except Exception as e:
            logger.error(f"Error sending backup to admins: {e}")

    async def scheduled_backup_task(self) -> None:
        """Task to run scheduled backups."""
        try:
            logger.info("Running scheduled backup check...")

            config = await self.get_bot_config_async()
            if not config.is_active:
                logger.info("Bot is inactive, skipping scheduled backup")
                return

            if not config.should_run_backup():
                logger.info("Not time for backup yet")
                return

            logger.info("Creating scheduled backup...")

            try:
                # Create backup and get result
                backup_result = await sync_to_async(create_database_backup)()

                if backup_result['success']:
                    logger.info("Scheduled backup completed successfully")

                    # Update last backup time
                    await self.update_bot_config(last_backup_at=timezone.now())

                    # Send backup file to admins
                    await self.send_backup_to_admins(
                        backup_path=backup_result['backup_path'],
                        filename=backup_result['backup_filename']
                    )

                    # Notify admins of success
                    success_msg = format_backup_result_markdown(backup_result)
                    for admin_id in config.admin_chat_ids:
                        try:
                            await self.application.bot.send_message(
                                chat_id=admin_id,
                                text=f"🔄 Scheduled Backup Completed\n\n{success_msg}",
                                parse_mode='Markdown'
                            )
                        except Exception as notify_error:
                            logger.error(f"Failed to notify admin {admin_id}: {notify_error}")
                else:
                    raise Exception(backup_result.get('error', 'Unknown backup error'))

            except Exception as e:
                logger.error(f"Scheduled backup failed: {e}")

                # Notify admins of failure
                for admin_id in config.admin_chat_ids:
                    try:
                        await self.application.bot.send_message(
                            chat_id=admin_id,
                            text=f"❌ Scheduled backup failed: {str(e)}"
                        )
                    except Exception as notify_error:
                        logger.error(f"Failed to notify admin {admin_id}: {notify_error}")

        except Exception as e:
            logger.error(f"Error in scheduled backup task: {e}")

    async def setup_application(self) -> Application:
        """Setup Telegram application with handlers."""
        application = Application.builder().token(self.bot_config.bot_token).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("ping", self.ping_command))
        application.add_handler(CommandHandler("backup", self.backup_command))

        # Add callback query handler for inline buttons
        application.add_handler(CallbackQueryHandler(self.callback_query_handler))

        self.application = application
        return application

    async def run_scheduler_loop(self) -> None:
        """Run the scheduler loop for automated tasks."""
        while True:
            try:
                # Check if scheduled backup should run
                config = await self.get_bot_config_async()
                if config.should_run_backup():
                    # Create task for backup (don't await to avoid blocking)
                    asyncio.create_task(self.scheduled_backup_task())

                # Wait before next check (every 5 minutes)
                await asyncio.sleep(300)

            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(60)  # Wait a minute before retrying

    async def run_bot(self) -> None:
        """Main method to run the bot."""
        try:
            logger.info("Starting Telegram bot...")

            # Setup application
            application = await self.setup_application()

            # Start the scheduler in background
            scheduler_task = asyncio.create_task(self.run_scheduler_loop())

            logger.info("Bot is running and listening for messages...")

            # Run the bot
            await application.run_polling(allowed_updates=Update.ALL_TYPES)

        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            raise
        finally:
            # Cancel scheduler task
            if 'scheduler_task' in locals():
                scheduler_task.cancel()
                try:
                    await scheduler_task
                except asyncio.CancelledError:
                    pass


class Command(BaseCommand):
    """
    Django management command to run the Telegram bot.
    """

    help = 'Run the Telegram bot for server monitoring and backup management'

    def add_arguments(self, parser):
        parser.add_argument(
            '--bot-id',
            type=int,
            help='Specific bot configuration ID to use (optional, uses first active bot if not specified)',
        )

    def handle(self, *args, **options):
        try:
            # Get bot configuration
            bot_id = options.get('bot_id')

            if bot_id:
                bot_config = TelegramBot.objects.get(pk=bot_id, is_active=True)
            else:
                bot_config = TelegramBot.objects.filter(is_active=True).first()

            if not bot_config:
                self.stderr.write(
                    self.style.ERROR('No active Telegram bot configuration found.')
                )
                return

            self.stdout.write(
                self.style.SUCCESS(f'Starting bot: {bot_config}')
            )

            # Create bot handler
            bot_handler = TelegramBotHandler(bot_config)

            # Run the bot (this will block until interrupted)
            asyncio.run(bot_handler.run_bot())

        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('Bot stopped by user')
            )
        except TelegramBot.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(f'Bot configuration with ID {bot_id} not found.')
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'Bot failed to start: {e}')
            )
            logger.error(f"Bot startup failed: {e}")
            raise
