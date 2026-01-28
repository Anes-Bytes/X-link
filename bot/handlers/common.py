from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from bot.keyboards.inline import get_main_menu
from bot.services.admin_service import AdminService
from bot.config import OWNER_ID

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    if not await AdminService.is_admin(message.from_user.id):
        return
    await message.answer("👋 خوش آمدید به پنل مدیریت X-Link", reply_markup=get_main_menu())

@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    if not await AdminService.is_admin(callback.from_user.id):
        return
    await callback.message.edit_text("👋 خوش آمدید به پنل مدیریت X-Link", reply_markup=get_main_menu())
    await callback.answer()
