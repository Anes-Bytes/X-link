import os
import zipfile
import psutil
import platform
import time
import subprocess
from datetime import datetime
from django.conf import settings

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
    """Creates a ZIP backup of the database and media folder."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_{timestamp}.zip"
    backup_path = os.path.join(settings.BASE_DIR, 'backups', backup_filename)
    
    if not os.path.exists(os.path.join(settings.BASE_DIR, 'backups')):
        os.makedirs(os.path.join(settings.BASE_DIR, 'backups'))

    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Backup Database
        db_path = settings.DATABASES['default']['NAME']
        if os.path.exists(db_path):
            zipf.write(db_path, os.path.basename(db_path))
        
        # Backup Media folder
        media_root = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(media_root))
                zipf.write(file_path, arcname)

    return backup_path, backup_filename

def get_site_stats():
    """Returns basic site statistics from Django models."""
    from core.models import CustomUser
    from cards.models import UserCard, Skill, Service, Portfolio
    
    return {
        'users_count': CustomUser.objects.count(),
        'cards_count': UserCard.objects.count(),
        'skills_count': Skill.objects.count(),
        'services_count': Service.objects.count(),
        'portfolios_count': Portfolio.objects.count(),
    }
