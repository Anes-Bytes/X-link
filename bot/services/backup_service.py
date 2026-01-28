import os
import shutil
import zipfile
import asyncio
from datetime import datetime
from pathlib import Path
from bot.config import DEBUG, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, BASE_DIR, MEDIA_DIR

class BackupService:
    @staticmethod
    async def create_backup() -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = BASE_DIR / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        temp_dir = backup_dir / f"temp_{timestamp}"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # 1. Database Backup
            if DEBUG:
                # SQLite
                db_path = BASE_DIR / "db.sqlite3"
                if db_path.exists():
                    shutil.copy2(db_path, temp_dir / "db.sqlite3")
            else:
                # MySQL
                dump_file = temp_dir / "db_dump.sql"
                # Note: This assumes mysqldump is in PATH
                # Windows might need .exe suffix or full path if not in PATH
                cmd = f"mysqldump -h {DB_HOST} -P {DB_PORT} -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} > {dump_file}"
                process = await asyncio.create_subprocess_shell(cmd)
                await process.communicate()

            # 2. Media Backup
            if MEDIA_DIR.exists():
                shutil.copytree(MEDIA_DIR, temp_dir / "media", dirs_exist_ok=True)

            # 3. Zip Compression
            zip_filename = backup_dir / f"backup_{timestamp}.zip"
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = Path(root) / file
                        zipf.write(file_path, file_path.relative_to(temp_dir))
            
            return str(zip_filename)
        
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

    @staticmethod
    def cleanup_old_backups(keep_days=7):
        # Implementation for cleaning up old zip files if needed
        pass
