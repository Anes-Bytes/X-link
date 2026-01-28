from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔐 مدیریت ادمین‌ها", callback_data="admin_mgmt"))
    builder.row(InlineKeyboardButton(text="📦 پشتیبان‌گیری", callback_data="backup_mgmt"))
    builder.row(InlineKeyboardButton(text="📊 وضعیت سرور", callback_data="server_status"))
    builder.row(InlineKeyboardButton(text="⚙️ تنظیمات", callback_data="settings"))
    return builder.as_markup()

def get_admin_mgmt_menu(is_owner: bool):
    builder = InlineKeyboardBuilder()
    if is_owner:
        builder.row(InlineKeyboardButton(text="➕ افزودن ادمین", callback_data="add_admin"))
        builder.row(InlineKeyboardButton(text="➖ حذف ادمین", callback_data="remove_admin"))
    builder.row(InlineKeyboardButton(text="📜 لیست ادمین‌ها", callback_data="list_admins"))
    builder.row(InlineKeyboardButton(text="🏠 منوی اصلی", callback_data="main_menu"))
    return builder.as_markup()

def get_backup_menu():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📦 پشتیبان‌گیری فوری", callback_data="instant_backup"))
    builder.row(InlineKeyboardButton(text="🕒 تنظیم بازه زمانی", callback_data="set_backup_interval"))
    builder.row(InlineKeyboardButton(text="📢 تنظیم کانال پشتیبان", callback_data="set_backup_channel"))
    builder.row(InlineKeyboardButton(text="🏠 منوی اصلی", callback_data="main_menu"))
    return builder.as_markup()

def get_back_button(target: str = "main_menu"):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ بازگشت", callback_data=target))
    builder.row(InlineKeyboardButton(text="🏠 منوی اصلی", callback_data="main_menu"))
    return builder.as_markup()

def get_confirmation_keyboard(action: str, value: str):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ تایید", callback_data=f"confirm_{action}_{value}"),
        InlineKeyboardButton(text="❌ لغو", callback_data="main_menu")
    )
    return builder.as_markup()
