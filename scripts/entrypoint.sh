#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Fix permissions
echo "Fixing permissions..."
chown -R www-data:www-data /app/logs /app/staticfiles /app/media /app

# Start Apache
echo "Starting Apache..."
exec apache2ctl -D FOREGROUND
