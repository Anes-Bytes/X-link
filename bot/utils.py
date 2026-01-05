import os
import zipfile
import psutil
import platform
import time
import subprocess
import pymysql
from datetime import datetime
from django.conf import settings
from environs import Env

env = Env.read_env()

def get_system_stats():
    """Returns CPU, RAM, Disk usage and Ping."""
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Simple ping check to google.com
    try:
        if platform.system().lower() == "windows":
            ping_cmd = ["ping", "-n", "1", "8.8.8.8"]
        else:
            ping_cmd = ["ping", "-c", "1", "8.8.8.8"]
        
        start = time.time()
        subprocess.run(ping_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        ping_time = round((time.time() - start) * 1000, 2)
    except Exception:
        ping_time = "N/A"

    return {
        'cpu': cpu_usage,
        'ram_percent': ram.percent,
        'ram_used': round(ram.used / (1024**3), 2),
        'ram_total': round(ram.total / (1024**3), 2),
        'disk_percent': disk.percent,
        'disk_used': round(disk.used / (1024**3), 2),
        'disk_total': round(disk.total / (1024**3), 2),
        'ping': ping_time
    }

def create_backup():
    """Creates a ZIP backup of both SQLite and MySQL databases and media folder."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_{timestamp}.zip"
    backup_path = os.path.join(settings.BASE_DIR, 'backups', backup_filename)

    if not os.path.exists(os.path.join(settings.BASE_DIR, 'backups')):
        os.makedirs(os.path.join(settings.BASE_DIR, 'backups'))

    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        try:
            # Backup SQLite database (bot data)
            bot_db_path = os.path.join(settings.BASE_DIR, 'bot_data.sqlite3')
            if os.path.exists(bot_db_path):
                zipf.write(bot_db_path, 'bot_data.sqlite3')

            # Backup Django database (SQLite or MySQL)
            db_engine = settings.DATABASES['default']['ENGINE']

            if 'sqlite3' in db_engine:
                # Backup SQLite database
                db_path = settings.DATABASES['default']['NAME']
                if os.path.exists(db_path):
                    zipf.write(db_path, 'db.sqlite3')
            elif 'mysql' in db_engine:
                # Backup MySQL database
                try:
                    mysql_backup_path = os.path.join(settings.BASE_DIR, 'backups', f'mysql_backup_{timestamp}.sql')

                    # Get MySQL credentials from .env
                    mysql_host = env.str('MYSQL_HOST', 'localhost')
                    mysql_port = env.int('MYSQL_PORT', 3306)
                    mysql_user = env.str('MYSQL_USER', 'root')
                    mysql_password = env.str('MYSQL_PASSWORD', '')
                    mysql_database = env.str('MYSQL_DATABASE', 'xlink_db')

                    # Create MySQL dump
                    import subprocess
                    mysqldump_cmd = [
                        'mysqldump',
                        '-h', mysql_host,
                        '-P', str(mysql_port),
                        '-u', mysql_user,
                        '-p' + mysql_password,
                        mysql_database
                    ]

                    with open(mysql_backup_path, 'w') as f:
                        subprocess.run(mysqldump_cmd, stdout=f, check=True)

                    # Add MySQL dump to ZIP
                    zipf.write(mysql_backup_path, 'mysql_backup.sql')

                    # Clean up temporary MySQL dump file
                    if os.path.exists(mysql_backup_path):
                        os.remove(mysql_backup_path)

                except Exception as e:
                    print(f"Warning: Could not backup MySQL database: {e}")
                    # Continue with media backup even if MySQL fails

        except Exception as e:
            print(f"Warning: Database backup failed: {e}")
            # Continue with media backup

        # Backup Media folder
        try:
            media_root = settings.MEDIA_ROOT
            if os.path.exists(media_root):
                for root, dirs, files in os.walk(media_root):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(media_root))
                        zipf.write(file_path, arcname)
        except Exception as e:
            print(f"Warning: Media backup failed: {e}")

    return backup_path, backup_filename

def get_site_stats():
    """Returns basic site statistics from Django models."""
    try:
        from core.models import CustomUser
        from cards.models import UserCard, Skill, Service, Portfolio

        return {
            'users_count': CustomUser.objects.count(),
            'cards_count': UserCard.objects.count(),
        }
    except Exception as e:
        print(f"Error getting site stats: {e}")
        return {
            'users_count': 0,
            'cards_count': 0,
        }
