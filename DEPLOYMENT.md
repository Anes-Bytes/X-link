# راهنمای استقرار پروژه X-link

این راهنما برای راه‌اندازی پروژه در محیط لینوکس (اوبونتو) با استفاده از **Nginx** و **Gunicorn** تهیه شده است.

## ۱. پیش‌نیازها
ابتدا پکیج‌های مورد نیاز سیستم را نصب کنید:
```bash
sudo apt update
sudo apt install nginx python3-pip python3-venv certbot python3-certbot-nginx
```

## ۲. آماده‌سازی پروژه
یک محیط مجازی بسازید و وابستگی‌ها را نصب کنید:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn setproctitle
```

فایل‌های استاتیک را جمع‌آوری کنید:
```bash
python manage.py collectstatic
```

## ۳. تنظیم Gunicorn (Systemd)
یک فایل سرویس برای گونی‌کورن بسازید:
`sudo nano /etc/systemd/system/gunicorn.service`

محتویات زیر را با جایگزین کردن مسیرهای صحیح قرار دهید:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=deploy
Group=www-data
WorkingDirectory=/home/deploy/X-link
ExecStart=/home/deploy/X-link/venv/bin/gunicorn \
          --config gunicorn_config.py \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

فعال‌سازی سرویس:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## ۴. تنظیم Nginx
فایل کانفیگ را کپی کنید:
```bash
sudo cp nginx.conf /etc/nginx/sites-available/x-link
sudo ln -s /etc/nginx/sites-available/x-link /etc/nginx/sites-enabled
```

تست و ری‌استارت انجین‌اکس:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

## ۵. نصب SSL (Certbot)
برای فعال‌سازی HTTPS رایگان:
```bash
sudo certbot --nginx -d x-link.ir -d www.x-link.ir
```

## نکات بهینه‌سازی:
- **Gunicorn**: از کلاس `gthread` استفاده شده که برای پردازش‌های I/O بسیار بهینه است.
- **Nginx**: فشرده‌سازی `gzip` و کش کردن فایل‌های استاتیک برای ۳۰ روز تنظیم شده است.
- **Security**: پروتکل‌های قدیمی SSL غیرفعال شده و فقط TLS 1.2 و 1.3 مجاز هستند.
