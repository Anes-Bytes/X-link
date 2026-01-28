from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.inline import get_admin_mgmt_menu, get_back_button, get_confirmation_keyboard
from bot.services.admin_service import AdminService
from bot.config import OWNER_ID

router = Router()

class AdminStates(StatesGroup):
    waiting_for_add_id = State()
    waiting_for_remove_id = State()

@router.callback_query(F.data == "admin_mgmt")
async def admin_mgmt_menu(callback: CallbackQuery):
    is_owner = callback.from_user.id == OWNER_ID
    await callback.message.edit_text("🔐 مدیریت ادمین‌ها", reply_markup=get_admin_mgmt_menu(is_owner))
    await callback.answer()

@router.callback_query(F.data == "add_admin")
async def start_add_admin(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != OWNER_ID:
        return await callback.answer("❌ فقط مالک ربات مجاز است", show_alert=True)
    
    await callback.message.edit_text("🔢 لطفا آیدی عددی تلگرام ادمین جدید را وارد کنید:", reply_markup=get_back_button("admin_mgmt"))
    await state.set_state(AdminStates.waiting_for_add_id)
    await callback.answer()

@router.message(AdminStates.waiting_for_add_id)
async def process_add_admin(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ لطفا فقط عدد وارد کنید.")
    
    target_id = int(message.text)
    await AdminService.add_admin(target_id)
    await message.answer(f"✅ ادمین با آیدی {target_id} با موفقیت اضافه شد.", reply_markup=get_back_button("admin_mgmt"))
    await state.clear()

@router.callback_query(F.data == "remove_admin")
async def start_remove_admin(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != OWNER_ID:
        return await callback.answer("❌ فقط مالک ربات مجاز است", show_alert=True)
    
    await callback.message.edit_text("🔢 لطفا آیدی عددی تلگرام ادمین را برای حذف وارد کنید:", reply_markup=get_back_button("admin_mgmt"))
    await state.set_state(AdminStates.waiting_for_remove_id)
    await callback.answer()

@router.message(AdminStates.waiting_for_remove_id)
async def process_remove_admin(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ لطفا فقط عدد وارد کنید.")
    
    target_id = int(message.text)
    await AdminService.remove_admin(target_id)
    await message.answer(f"✅ ادمین با آیدی {target_id} با موفقیت حذف شد.", reply_markup=get_back_button("admin_mgmt"))
    await state.clear()

@router.callback_query(F.data == "list_admins")
async def list_admins(callback: CallbackQuery):
    admins = await AdminService.get_all_admins()
    text = "📜 **لیست ادمین‌ها:**\n\n"
    for admin in admins:
        text += f"👤 ID: `{admin.telegram_id}`\n"
    
    if not admins:
        text += "لیست خالی است."
        
    await callback.message.edit_text(text, reply_markup=get_back_button("admin_mgmt"), parse_mode="Markdown")
    await callback.answer()
