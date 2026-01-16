# Deployment Guide

This guide covers deploying LegalDocs Manager to a production environment.

## Table of Contents

- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Production Settings](#production-settings)
- [Web Server Configuration](#web-server-configuration)
- [Static Files & Media](#static-files--media)
- [Security Recommendations](#security-recommendations)
- [Monitoring & Logging](#monitoring--logging)
- [Backup Strategy](#backup-strategy)
- [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

Complete these steps before deploying to production:

### Code Preparation

- [ ] All tests pass: `python manage.py test`
- [ ] Code coverage meets minimum threshold (70%+)
- [ ] No DEBUG statements in production code
- [ ] All migrations are created and tested
- [ ] requirements.txt is up to date

### Environment Setup

- [ ] Production server provisioned (Linux recommended)
- [ ] Python 3.11+ installed
- [ ] PostgreSQL 15+ installed and configured
- [ ] Domain name configured (DNS pointing to server)
- [ ] SSL/TLS certificate obtained (Let's Encrypt recommended)

### Security Audit

- [ ] SECRET_KEY is unique and secure (not in version control)
- [ ] DEBUG is set to False
- [ ] ALLOWED_HOSTS configured correctly
- [ ] Database credentials are secure
- [ ] File upload restrictions in place
- [ ] CORS settings reviewed

---

## Environment Variables

Create a `.env` file on your production server (never commit to version control):

```bash
# Django Core Settings
SECRET_KEY=your-unique-secret-key-minimum-50-characters
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DATABASE_URL=postgres://user:password@localhost:5432/legaldocs_prod
# Or individual settings:
DB_NAME=legaldocs_prod
DB_USER=legaldocs_user
DB_PASSWORD=secure-database-password
DB_HOST=localhost
DB_PORT=5432

# Security Settings
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email Configuration (for password reset, notifications)
EMAIL_HOST=smtp.yourmailprovider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# File Storage
MEDIA_ROOT=/var/www/legaldocs/media
STATIC_ROOT=/var/www/legaldocs/static
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes

# Optional: Sentry for error tracking
SENTRY_DSN=https://your-sentry-dsn
```

### Generating a Secure SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Database Setup

### PostgreSQL Installation (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Create Database and User

```bash
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE legaldocs_prod;
CREATE USER legaldocs_user WITH PASSWORD 'secure-password';
ALTER ROLE legaldocs_user SET client_encoding TO 'utf8';
ALTER ROLE legaldocs_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE legaldocs_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE legaldocs_prod TO legaldocs_user;
\q
```

### Run Migrations

```bash
cd /var/www/legaldocs
source venv/bin/activate
python manage.py migrate --settings=legaldocs.settings_prod
```

---

## Production Settings

Create `legaldocs/settings_prod.py`:

```python
from .settings import *
import os

# Security settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'legaldocs_prod'),
        'USER': os.environ.get('DB_USER', 'legaldocs_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 60,
    }
}

# Static and media files
STATIC_ROOT = os.environ.get('STATIC_ROOT', '/var/www/legaldocs/static')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/var/www/legaldocs/media')

# Security middleware settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/legaldocs/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'WARNING',
    },
}
```

---

## Web Server Configuration

### Using Gunicorn + Nginx (Recommended)

#### Install Gunicorn

```bash
pip install gunicorn
```

#### Gunicorn Service File

Create `/etc/systemd/system/legaldocs.service`:

```ini
[Unit]
Description=LegalDocs Manager Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/legaldocs/legaldocs
EnvironmentFile=/var/www/legaldocs/.env
ExecStart=/var/www/legaldocs/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/gunicorn/legaldocs.sock \
    --access-logfile /var/log/legaldocs/gunicorn-access.log \
    --error-logfile /var/log/legaldocs/gunicorn-error.log \
    legaldocs.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Gunicorn

```bash
sudo mkdir -p /run/gunicorn
sudo chown www-data:www-data /run/gunicorn
sudo systemctl daemon-reload
sudo systemctl start legaldocs
sudo systemctl enable legaldocs
```

#### Nginx Configuration

Create `/etc/nginx/sites-available/legaldocs`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/legaldocs/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/legaldocs/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://unix:/run/gunicorn/legaldocs.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/legaldocs /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Static Files & Media

### Collect Static Files

```bash
cd /var/www/legaldocs
source venv/bin/activate
python manage.py collectstatic --settings=legaldocs.settings_prod --noinput
```

### Media Directory Permissions

```bash
sudo mkdir -p /var/www/legaldocs/media
sudo chown -R www-data:www-data /var/www/legaldocs/media
sudo chmod -R 755 /var/www/legaldocs/media
```

---

## Security Recommendations

### Essential Security Measures

1. **Keep software updated**
   ```bash
   sudo apt update && sudo apt upgrade
   pip install --upgrade -r requirements.txt
   ```

2. **Use strong passwords**
   - Database: Minimum 20 characters, mixed case, numbers, symbols
   - Admin accounts: Require strong passwords via Django validators

3. **Firewall configuration (UFW)**
   ```bash
   sudo ufw allow 22/tcp    # SSH
   sudo ufw allow 80/tcp    # HTTP (redirects to HTTPS)
   sudo ufw allow 443/tcp   # HTTPS
   sudo ufw enable
   ```

4. **Fail2ban for brute force protection**
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

5. **Regular security audits**
   ```bash
   pip install safety
   safety check -r requirements.txt
   ```

### API Security

- Token authentication is required for all API endpoints
- Tokens expire and should be rotated periodically
- Rate limiting recommended for production (use django-ratelimit)
- CORS is configured to restrict cross-origin requests

### File Upload Security

- Allowed file types are restricted (PDF, DOC, DOCX, etc.)
- Maximum file size is enforced (default: 10MB)
- Files are stored outside the web root
- File names are sanitized to prevent directory traversal

---

## Monitoring & Logging

### Log Files

| Log | Location | Purpose |
|-----|----------|---------|
| Django | `/var/log/legaldocs/django.log` | Application errors |
| Gunicorn Access | `/var/log/legaldocs/gunicorn-access.log` | HTTP requests |
| Gunicorn Error | `/var/log/legaldocs/gunicorn-error.log` | Worker errors |
| Nginx Access | `/var/log/nginx/access.log` | All HTTP traffic |
| Nginx Error | `/var/log/nginx/error.log` | Proxy errors |

### Create Log Directory

```bash
sudo mkdir -p /var/log/legaldocs
sudo chown www-data:www-data /var/log/legaldocs
```

### Log Rotation

Create `/etc/logrotate.d/legaldocs`:

```
/var/log/legaldocs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload legaldocs
    endscript
}
```

### Recommended Monitoring Tools

- **Sentry**: Error tracking and alerting
- **Prometheus + Grafana**: Metrics and dashboards
- **UptimeRobot**: Availability monitoring

---

## Backup Strategy

### Database Backups

Create `/usr/local/bin/backup-legaldocs.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/legaldocs"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U legaldocs_user legaldocs_prod | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Media files backup
tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" /var/www/legaldocs/media

# Remove old backups
find $BACKUP_DIR -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: $DATE"
```

### Automated Backups (Cron)

```bash
sudo chmod +x /usr/local/bin/backup-legaldocs.sh
sudo crontab -e

# Add this line for daily backups at 2 AM:
0 2 * * * /usr/local/bin/backup-legaldocs.sh >> /var/log/legaldocs/backup.log 2>&1
```

### Restore from Backup

```bash
# Database restore
gunzip -c /var/backups/legaldocs/db_YYYYMMDD_HHMMSS.sql.gz | psql -U legaldocs_user legaldocs_prod

# Media restore
tar -xzf /var/backups/legaldocs/media_YYYYMMDD_HHMMSS.tar.gz -C /
```

---

## Troubleshooting

### Common Issues

#### 500 Internal Server Error

1. Check Django logs: `tail -f /var/log/legaldocs/django.log`
2. Check Gunicorn logs: `tail -f /var/log/legaldocs/gunicorn-error.log`
3. Verify environment variables are set
4. Ensure migrations are applied

#### Static Files Not Loading

1. Run `collectstatic`: `python manage.py collectstatic --noinput`
2. Check Nginx static file configuration
3. Verify file permissions: `ls -la /var/www/legaldocs/static/`

#### Database Connection Failed

1. Verify PostgreSQL is running: `systemctl status postgresql`
2. Check database credentials in `.env`
3. Test connection: `psql -U legaldocs_user -h localhost legaldocs_prod`

#### Permission Denied Errors

```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/legaldocs

# Fix permissions
sudo chmod -R 755 /var/www/legaldocs
sudo chmod 600 /var/www/legaldocs/.env
```

### Health Check Endpoint

The API provides a health check at `/api/dashboard/` (requires authentication).

For unauthenticated health checks, consider adding a simple view:

```python
# In api/views.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})

# In api/urls.py
path('health/', health_check, name='health-check'),
```

---

## Deployment Verification

After deployment, verify:

1. **API Health**: `curl https://yourdomain.com/api/auth/register/`
2. **Static Files**: Check CSS/JS loads in browser
3. **Media Uploads**: Test file upload via API
4. **Database**: Verify data persists across restarts
5. **SSL**: Check certificate with `curl -I https://yourdomain.com`
6. **Logs**: Ensure logs are being written

### Quick Test Commands

```bash
# Test API is responding
curl -I https://yourdomain.com/api/

# Check SSL certificate
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Check Gunicorn status
sudo systemctl status legaldocs

# Check Nginx status
sudo systemctl status nginx
```

---

## Support

For issues or questions:
- Check the logs first
- Review this guide's troubleshooting section
- Open an issue in the project repository
