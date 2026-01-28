import psutil
import platform
import time
from datetime import datetime

class MonitorService:
    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_ram_usage():
        ram = psutil.virtual_memory()
        return {
            "percent": ram.percent,
            "used": ram.used / (1024 ** 3),
            "total": ram.total / (1024 ** 3)
        }

    @staticmethod
    def get_disk_usage():
        disk = psutil.disk_usage('/')
        return {
            "percent": disk.percent,
            "used": disk.used / (1024 ** 3),
            "total": disk.total / (1024 ** 3)
        }

    @staticmethod
    def get_uptime():
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        
        days, rem = divmod(uptime_seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)
        
        return f"{int(days)}d {int(hours)}h {int(minutes)}m"

    @staticmethod
    def get_load_average():
        try:
            if platform.system() != "Windows":
                import os
                return os.getloadavg()
            return "N/A on Windows"
        except Exception:
            return "N/A"

    @classmethod
    def get_server_status(cls):
        cpu = cls.get_cpu_usage()
        ram = cls.get_ram_usage()
        disk = cls.get_disk_usage()
        uptime = cls.get_uptime()
        
        return (
            f"📊 **Server Status**\n\n"
            f"💻 CPU: {cpu}%\n"
            f"🧠 RAM: {ram['percent']}% ({ram['used']:.2f}/{ram['total']:.2f} GB)\n"
            f"💾 Disk: {disk['percent']}% ({disk['used']:.2f}/{disk['total']:.2f} GB)\n"
            f"🕒 Uptime: {uptime}\n"
        )
