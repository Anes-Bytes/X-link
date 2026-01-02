"""
Server monitoring and backup utility functions for the Telegram bot.
"""

import os
import shutil
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


def get_server_resources() -> Dict[str, Any]:
    """
    Get comprehensive server resource information.

    Returns:
        dict: Dictionary containing server resource data
    """
    try:
        import psutil

        # CPU Information
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_count_logical = psutil.cpu_count(logical=True)

        # Memory Information
        memory = psutil.virtual_memory()
        memory_info = {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': memory.percent,
            'total_gb': round(memory.total / (1024**3), 2),
            'used_gb': round(memory.used / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2)
        }

        # Disk Information
        disk = psutil.disk_usage('/')
        disk_info = {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent,
            'total_gb': round(disk.total / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2)
        }

        # Network Information
        network = psutil.net_io_counters()
        network_info = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv,
            'sent_mb': round(network.bytes_sent / (1024**2), 2),
            'recv_mb': round(network.bytes_recv / (1024**2), 2)
        }

        # System Information
        system_info = {
            'boot_time': psutil.boot_time(),
            'uptime_seconds': psutil.time.time() - psutil.boot_time()
        }

        return {
            'success': True,
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'count_logical': cpu_count_logical
            },
            'memory': memory_info,
            'disk': disk_info,
            'network': network_info,
            'system': system_info
        }

    except ImportError:
        return {
            'success': False,
            'error': 'psutil not installed. Please install psutil for server monitoring.',
            'error_type': 'missing_dependency'
        }
    except Exception as e:
        logger.error(f"Error getting server resources: {e}")
        return {
            'success': False,
            'error': f'Error getting server resources: {str(e)}',
            'error_type': 'runtime_error'
        }


def format_server_resources_markdown(data: Dict[str, Any]) -> str:
    """
    Format server resource data as Markdown text for Telegram.

    Args:
        data: Server resource data from get_server_resources()

    Returns:
        str: Formatted markdown text
    """
    if not data.get('success', False):
        return f"❌ {data.get('error', 'Unknown error')}"

    cpu = data['cpu']
    memory = data['memory']
    disk = data['disk']
    network = data['network']
    system = data['system']

    # Calculate uptime
    uptime_hours = int(system['uptime_seconds'] // 3600)
    uptime_minutes = int((system['uptime_seconds'] % 3600) // 60)

    return (
        f"🖥️ *CPU:* {cpu['percent']:.1f}% ({cpu['count']} cores)\n"
        f"🧠 *RAM:* {memory['used_gb']:.1f}GB/{memory['total_gb']:.1f}GB ({memory['percent']:.1f}%)\n"
        f"💽 *Disk:* {disk['used_gb']:.1f}GB/{disk['total_gb']:.1f}GB ({disk['percent']:.1f}%)\n"
        f"🌐 *Network:* ↑{network['sent_mb']:.1f}MB ↓{network['recv_mb']:.1f}MB\n"
        f"⏰ *Uptime:* {uptime_hours}h {uptime_minutes}m\n"
        f"📅 *Updated:* {datetime.now().strftime('%H:%M:%S')}"
    )


def create_database_backup(backup_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a backup of the SQLite database.

    Args:
        backup_dir: Directory to store backup (optional, defaults to 'backups' in BASE_DIR)

    Returns:
        dict: Backup result information
    """
    try:
        from django.conf import settings

        # Get database path
        db_path = settings.DATABASES['default']['NAME']

        if not os.path.exists(db_path):
            return {
                'success': False,
                'error': 'Database file not found',
                'error_type': 'file_not_found'
            }

        # Create backup directory
        if backup_dir is None:
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')

        os.makedirs(backup_dir, exist_ok=True)

        # Generate backup filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"db_backup_{timestamp}.sqlite3"
        backup_path = os.path.join(backup_dir, backup_filename)

        # Copy database file
        shutil.copy2(db_path, backup_path)

        # Get file information
        file_size = os.path.getsize(backup_path)
        file_size_mb = round(file_size / (1024**2), 2)

        # Verify backup integrity (basic check)
        if not os.path.exists(backup_path) or os.path.getsize(backup_path) == 0:
            return {
                'success': False,
                'error': 'Backup file was not created or is empty',
                'error_type': 'backup_verification_failed'
            }

        return {
            'success': True,
            'backup_path': backup_path,
            'backup_filename': backup_filename,
            'file_size': file_size,
            'file_size_mb': file_size_mb,
            'timestamp': datetime.now(),
            'backup_dir': backup_dir
        }

    except Exception as e:
        logger.error(f"Database backup failed: {e}")
        return {
            'success': False,
            'error': f'Backup failed: {str(e)}',
            'error_type': 'backup_error'
        }


def format_backup_result_markdown(result: Dict[str, Any]) -> str:
    """
    Format backup result as Markdown text for Telegram.

    Args:
        result: Backup result from create_database_backup()

    Returns:
        str: Formatted markdown text
    """
    if not result.get('success', False):
        return f"❌ {result.get('error', 'Unknown error')}"

    return (
        f"✅ *Database Backup Created Successfully!*\n\n"
        f"📁 *File:* {result['backup_filename']}\n"
        f"📊 *Size:* {result['file_size_mb']:.1f} MB\n"
        f"⏰ *Time:* {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"📍 *Location:* {result['backup_dir']}"
    )


def cleanup_old_backups(backup_dir: str, keep_days: int = 30) -> Dict[str, Any]:
    """
    Clean up old backup files.

    Args:
        backup_dir: Directory containing backup files
        keep_days: Number of days of backups to keep

    Returns:
        dict: Cleanup result information
    """
    try:
        if not os.path.exists(backup_dir):
            return {
                'success': True,
                'message': 'Backup directory does not exist',
                'files_removed': 0
            }

        cutoff_date = datetime.now() - timedelta(days=keep_days)
        files_removed = 0

        for filename in os.listdir(backup_dir):
            if filename.startswith('db_backup_') and filename.endswith('.sqlite3'):
                filepath = os.path.join(backup_dir, filename)

                # Extract timestamp from filename
                try:
                    timestamp_str = filename.replace('db_backup_', '').replace('.sqlite3', '')
                    file_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')

                    if file_date < cutoff_date:
                        os.remove(filepath)
                        files_removed += 1
                        logger.info(f"Removed old backup: {filename}")

                except (ValueError, OSError) as e:
                    logger.warning(f"Could not process backup file {filename}: {e}")

        return {
            'success': True,
            'message': f'Successfully removed {files_removed} old backup files',
            'files_removed': files_removed
        }

    except Exception as e:
        logger.error(f"Backup cleanup failed: {e}")
        return {
            'success': False,
            'error': f'Cleanup failed: {str(e)}',
            'error_type': 'cleanup_error'
        }


def ping_server(host: str = '8.8.8.8', timeout: int = 5) -> Dict[str, Any]:
    """
    Ping a server to check connectivity.

    Args:
        host: Host to ping (default: Google DNS)
        timeout: Timeout in seconds

    Returns:
        dict: Ping result information
    """
    try:
        import subprocess
        import platform

        # Determine ping command based on OS
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-W' if platform.system().lower() != 'windows' else '-w', str(timeout), host]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout + 1
        )

        success = result.returncode == 0

        return {
            'success': success,
            'host': host,
            'reachable': success,
            'timeout': timeout
        }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'host': host,
            'reachable': False,
            'timeout': timeout,
            'error': 'Ping timeout'
        }
    except Exception as e:
        logger.error(f"Ping failed: {e}")
        return {
            'success': False,
            'host': host,
            'reachable': False,
            'timeout': timeout,
            'error': f'Ping error: {str(e)}'
        }
