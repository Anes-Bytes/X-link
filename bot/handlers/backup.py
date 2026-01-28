import os
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.inline import get_backup_menu, get_back_button
from bot.services.backup_service import BackupService
from bot.database.models import BotSetting
from bot.config import BACKUP_CHANNEL_ID

router = Router()

class BackupStates(StatesGroup):
    waiting_for_channel_id = State()
    waiting_for_interval = State()

@router.callback_query(F.data == "backup_mgmt")
async def backup_mgmt_menu(callback: CallbackQuery):
    await callback.message.edit_text("📦 مدیریت پشتیبان‌گیری", reply_markup=get_backup_menu())
    await callback.answer()

@router.callback_query(F.data == "instant_backup")
async def instant_backup(callback: CallbackQuery, bot: Bot):
    await callback.message.edit_text("⏳ در حال تهیه پشتیبان... لطفا صبر کنید.")
    
    try:
        zip_path = await BackupService.create_backup()
        
        # Get backup channel ID from settings or config
        channel_id = await BotSetting.get_val("backup_channel_id", BACKUP_CHANNEL_ID)
        
        document = FSInputFile(zip_path)
        await bot.send_document(
            chat_id=channel_id,
            document=document,
            caption=f"📦 نسخه پشتیبان جدید\n📅 تاریخ: {os.path.basename(zip_path)}"
        )
        
        await callback.message.edit_text("✅ عملیات با موفقیت انجام شد و فایل به کانال ارسال گردید.", reply_markup=get_back_button("backup_mgmt"))
        
        # Cleanup
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
    except Exception as e:
        await callback.message.edit_text(f"❌ خطا در انجام عملیات: {str(e)}", reply_markup=get_back_button("backup_mgmt"))
    
    await callback.answer()

@router.callback_query(F.data == "set_backup_channel")
async def set_backup_channel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🆔 لطفا آیدی عددی کانال پشتیبان را وارد کنید (مثال: -100123456789):", reply_markup=get_back_button("backup_mgmt"))
    await state.set_state(BackupStates.waiting_for_channel_id)
    await callback.answer()

@router.message(BackupStates.waiting_for_channel_id)
async def process_set_channel(message: Message, state: FSMContext):
    try:
        channel_id = int(message.text)
        await BotSetting.set_val("backup_channel_id", channel_id)
        await message.answer(f"✅ کانال پشتیبان به آیدی {channel_id} تغییر یافت.", reply_markup=get_back_button("backup_mgmt"))
        await state.clear()
    except ValueError:
        await message.answer("❌ لطفا یک آیدی عددی معتبر وارد کنید.")

@router.callback_query(F.data == "set_backup_interval")
async def set_backup_interval(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("⏱ بازه زمانی پشتیبان‌گیری خودکار را به دقیقه وارد کنید (مثال: 60):", reply_markup=get_back_button("backup_mgmt"))
    await state.set_state(BackupStates.waiting_for_interval)
    await callback.answer()

@router.message(BackupStates.waiting_for_interval)
async def process_set_interval(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ لطفا فقط عدد وارد کنید.")
    
    interval = int(message.text)
    await BotSetting.set_val("backup_interval", interval)
    await message.answer(f"✅ بازه زمانی پشتیبان‌گیری به {interval} دقیقه تغییر یافت.", reply_markup=get_back_button("backup_mgmt"))
    await state.clear()
    # Note: Scheduler update will be needed
