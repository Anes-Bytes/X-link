import os
from pathlib import Path
from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

def get_int(key, default):
    val = env.str(key, default=str(default))
    if not val or val == "None":
        return default
    try:
        return int(val)
    except ValueError:
        return default

# Bot Settings
BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")
OWNER_ID = get_int("OWNER_ID", 0)
ADMIN_CHANNEL_ID = get_int("TELEGRAM_ADMIN_CHAT_IDS", 0)
DEBUG = env.bool("DEBUG", default=True)

# Database Settings
DB_NAME = env.str("DB_NAME", default="bot_db")
DB_USER = env.str("DB_USER", default="root")
DB_PASSWORD = env.str("DB_PASSWORD", default="")
DB_HOST = env.str("DB_HOST", default="localhost")
DB_PORT = get_int("DB_PORT", 3306)

def get_db_url():
    if DEBUG:
        return f"sqlite://{BASE_DIR}/db.sqlite3"
    return f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DATABASE_CONFIG = {
    "connections": {"default": get_db_url()},
    "apps": {
        "models": {
            "models": ["bot.database.models"],
            "default_connection": "default",
        }
    },
}

# Backup Settings
BACKUP_CHANNEL_ID = get_int("TELEGRAM_BACKUP_CHANNEL_ID", ADMIN_CHANNEL_ID)
BACKUP_INTERVAL = get_int("BACKUP_INTERVAL", 60)  # minutes
MEDIA_DIR = BASE_DIR / "media"
LOGS_DIR = BASE_DIR / "logs"
