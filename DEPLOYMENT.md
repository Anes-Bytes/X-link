# X-Link Full Deployment Guide (Ubuntu + Nginx + Gunicorn + PostgreSQL)

This guide deploys the `x-link` project on Ubuntu for:
- Root domain: `x-link.ir`
- Wildcard subdomains: `*.x-link.ir`
- Stack: `Django + Gunicorn + Nginx + PostgreSQL`

---

## 1. Prerequisites

### 1.1 Ubuntu packages
```bash
sudo apt update
sudo apt install -y \
  python3 python3-venv python3-pip \
  postgresql postgresql-contrib \
  nginx certbot python3-certbot-nginx
```

### 1.2 Server assumptions
- Project path: `/var/www/x-link`
- Linux user to run app: `www-data`
- Python venv path: `/var/www/x-link/.venv`

---

## 2. DNS Records (required for subdomains)

At your DNS provider, set:

1. `A` record  
`@  ->  <SERVER_PUBLIC_IP>`

2. `A` wildcard record  
`*  ->  <SERVER_PUBLIC_IP>`

3. `A` or `CNAME` for www  
`www -> @`

Optional if you use IPv6:
- `AAAA @ -> <SERVER_IPV6>`
- `AAAA * -> <SERVER_IPV6>`

Recommended TTL: `300` or `600`.

---

## 3. SSL for root + wildcard subdomain

You need certificate coverage for:
- `x-link.ir`
- `*.x-link.ir`

For wildcard, use DNS challenge (`DNS-01`), not plain HTTP challenge.

Example manual issuance:
```bash
sudo certbot certonly --manual --preferred-challenges dns \
  -d x-link.ir -d "*.x-link.ir"
```

Expected cert paths:
- `/etc/letsencrypt/live/x-link.ir/fullchain.pem`
- `/etc/letsencrypt/live/x-link.ir/privkey.pem`

---

## 4. Clone and setup project

```bash
sudo mkdir -p /var/www
cd /var/www
sudo git clone https://github.com/Anes-Bytes/X-link.git x-link
sudo chown -R $USER:$USER /var/www/x-link
cd /var/www/x-link
```

Create virtualenv and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. PostgreSQL setup

Create DB and user:
```bash
sudo -u postgres psql
CREATE DATABASE x_link_db;
CREATE USER x_link_user WITH PASSWORD 'CHANGE_THIS_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE x_link_db TO x_link_user;
\q
```

---

## 6. Environment variables (`.env`)

Create file:
```bash
cd /var/www/x-link
cp .env.example .env
```

Set at least these values:
```env
SECRET_KEY=CHANGE_ME
DEBUG=False

BASE_DOMAIN=x-link.ir
ALLOWED_HOSTS=x-link.ir,www.x-link.ir,.x-link.ir

DB_NAME=x_link_db
DB_USER=x_link_user
DB_PASSWORD=CHANGE_ME
DB_HOST=127.0.0.1
DB_PORT=5432
DB_CONN_MAX_AGE=60
DB_SSLMODE=prefer

SECURE_SSL_REDIRECT=True
```

Also fill third-party keys used by project:
- `MELIPAYAMAK_USERNAME`
- `MELIPAYAMAK_APIKEY`
- `MELIPAYAMAK_NUMBER`

---

## 7. Django migration and static files

```bash
cd /var/www/x-link
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## 8. Gunicorn (systemd service)

Project already contains:
- `deploy/systemd/gunicorn.service`

Install service:
```bash
sudo cp /var/www/x-link/deploy/systemd/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

---

## 9. Nginx config

Project already contains:
- `deploy/nginx/x-link.ir.conf`

Install and enable:
```bash
sudo cp /var/www/x-link/deploy/nginx/x-link.ir.conf /etc/nginx/sites-available/x-link.ir
sudo ln -sf /etc/nginx/sites-available/x-link.ir /etc/nginx/sites-enabled/x-link.ir
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

This config already has aliases:
- `/static/` -> `/var/www/x-link/staticfiles/`
- `/media/` -> `/var/www/x-link/media/`

---

## 10. Permissions

Ensure runtime paths are writable/readable:
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn
sudo chown -R www-data:www-data /var/www/x-link/media
sudo chown -R www-data:www-data /var/www/x-link/staticfiles
```

---

## 11. Health checks

```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo journalctl -u gunicorn -f
sudo tail -f /var/log/nginx/x-link.error.log
```

Quick app check:
```bash
curl -I https://x-link.ir
curl -I https://test.x-link.ir
```

---

## 12. Plan-expiry command (cron)

Run manually:
```bash
cd /var/www/x-link
source .venv/bin/activate
python manage.py check_user_plans
```

Dry run:
```bash
python manage.py check_user_plans --dry-run
```

Daily cron example (`02:00`):
```bash
0 2 * * * cd /var/www/x-link && /var/www/x-link/.venv/bin/python manage.py check_user_plans >> /var/log/x-link-plan-expiry.log 2>&1
```

---

## 13. Update / redeploy flow

```bash
cd /var/www/x-link
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl reload nginx
```

---

## 14. Common failures checklist

1. `DisallowedHost`:
- Check `ALLOWED_HOSTS` and `BASE_DOMAIN` in `.env`.

2. Static files not loading:
- Re-run `collectstatic`.
- Verify Nginx alias path.

3. Subdomain not resolving:
- Check wildcard DNS `* A`.
- Wait for DNS propagation.

4. SSL mismatch on subdomains:
- Ensure certificate includes `*.x-link.ir`.

5. DB connection errors:
- Verify PostgreSQL service is running:
```bash
sudo systemctl status postgresql
```
- Verify `.env` DB credentials.
