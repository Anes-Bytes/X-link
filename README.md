# X-Link Deployment Notes

## وضعیت کد ساب‌دامین

از نظر کد، مسیر اصلی ساب‌دامین‌ها در پروژه درست پیاده‌سازی شده است:

- اعتبارسنجی نام ساب‌دامین (`a-z`, `0-9`, `-` و طول 3 تا 30)
- جلوگیری از نام‌های رزرو شده (`admin`, `www`, ...)
- یونیک بودن ساب‌دامین در دیتابیس
- هندل همزمانی هنگام ثبت ساب‌دامین
- تشخیص ساب‌دامین از `Host` و روت کردن به `config.subdomain_urls`

نکات باقی‌مانده در کد/تنظیمات:

- مقدار `DEBUG` در `.env` باید معتبر باشد (`true` یا `false`)
- بهتر است روی endpoint بررسی ساب‌دامین rate-limit اضافه شود

---

## چک‌لیست دیپلوی صحیح ساب‌دامین

1. DNS
- `A` برای `x-link.ir` به IP سرور
- `A` برای `www` به IP سرور
- `A` برای `*` (wildcard) به IP سرور
- در صورت استفاده از IPv6، رکوردهای `AAAA` هم ست شود

2. SSL
- گواهی باید wildcard باشد: `*.x-link.ir` (به‌همراه `x-link.ir`)
- در غیر این صورت ساب‌دامین‌ها خطای SSL خواهند داشت

3. Nginx
- `server_name x-link.ir .x-link.ir;`
- ارسال `Host` به اپ: `proxy_set_header Host $host;`
- بعد از تغییرات:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

4. Environment
- `BASE_DOMAIN=x-link.ir`
- `ALLOWED_HOSTS=x-link.ir,www.x-link.ir,.x-link.ir`
- `DEBUG=False`
- در صورت نیاز به CSRF روی ساب‌دامین‌ها:
  `CSRF_TRUSTED_ORIGINS=https://*.x-link.ir`

5. Django

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

6. تست نهایی
- `https://x-link.ir`
- `https://test.x-link.ir`
- ساخت کارت جدید و باز شدن روی `username.x-link.ir`
- تست نام‌های رزرو (`admin`, `www`, ...)

---

## جمع‌بندی

مشکل اصلی برای کارکرد ساب‌دامین در production معمولاً DNS/SSL/Nginx است، نه منطق کد.
