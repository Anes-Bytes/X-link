from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.inline import get_back_button
from bot.services.monitor_service import MonitorService

router = Router()

@router.callback_query(F.data == "server_status")
async def server_status(callback: CallbackQuery):
    status_text = MonitorService.get_server_status()
    await callback.message.edit_text(status_text, reply_markup=get_back_button(), parse_mode="Markdown")
    await callback.answer()
