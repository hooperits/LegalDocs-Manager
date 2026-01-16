# Quickstart: Project Setup

**Feature**: 001-project-setup
**Date**: 2026-01-16

## Prerequisites

- Python 3.11+ installed
- PostgreSQL 15+ installed and running
- Git installed
- Terminal access

## Quick Setup (5 minutes)

### 1. Clone and Setup Environment

```bash
# Navigate to project
cd /home/juanca/proys/LegalDocs-Manager

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Run these SQL commands:
CREATE DATABASE legaldocs_db;
CREATE USER legaldocs_user WITH PASSWORD 'devpassword123';
ALTER ROLE legaldocs_user SET client_encoding TO 'utf8';
ALTER ROLE legaldocs_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE legaldocs_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE legaldocs_db TO legaldocs_user;
\c legaldocs_db
GRANT ALL ON SCHEMA public TO legaldocs_user;
\q
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
# Update DB_PASSWORD to match what you set above
```

### 4. Initialize Django

```bash
# Navigate to Django project
cd legaldocs

# Run migrations
python manage.py migrate

# Create superuser (follow prompts)
python manage.py createsuperuser
```

### 5. Start Development Server

```bash
# Start server
python manage.py runserver

# Access in browser:
# http://localhost:8000/admin/
```

## Verification Checklist

Run these commands to verify setup:

```bash
# Check Django configuration
python manage.py check
# Expected: "System check identified no issues"

# Verify database connection
python manage.py dbshell
# Should connect to PostgreSQL, type \q to exit

# List installed apps
python manage.py showmigrations
# Should show all Django apps with [X] for applied migrations
```

## Common Issues

### psycopg2 Installation Error

If `pip install psycopg2-binary` fails:

```bash
# On Ubuntu/Debian
sudo apt-get install libpq-dev python3-dev

# On macOS with Homebrew
brew install postgresql
```

### PostgreSQL Connection Refused

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start if not running
sudo systemctl start postgresql
```

### Permission Denied on Database

```bash
# Connect as postgres superuser
sudo -u postgres psql

# Grant permissions
GRANT ALL ON SCHEMA public TO legaldocs_user;
ALTER DATABASE legaldocs_db OWNER TO legaldocs_user;
```

## Project Structure After Setup

```
LegalDocs-Manager/
├── legaldocs/
│   ├── manage.py
│   ├── legaldocs/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── core/
│   ├── clients/
│   ├── cases/
│   ├── documents/
│   ├── users/
│   ├── static/
│   └── media/
├── venv/
├── .env
├── .env.example
├── .gitignore
└── requirements.txt
```

## Next Steps

After completing setup:

1. Verify Django Admin works at `/admin/`
2. Log in with superuser credentials
3. Proceed to feature `002-core-models` to create base models
