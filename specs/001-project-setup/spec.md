# Feature Specification: Project Setup

**Feature Branch**: `001-project-setup`
**Created**: 2026-01-16
**Status**: Draft
**Input**: Initial Django project setup with PostgreSQL, DRF, and essential packages

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Environment Setup (Priority: P1)

As a developer, I want to set up a complete Django development environment so that I can start building the LegalDocs Manager application with all required dependencies installed and configured.

**Why this priority**: Without a working development environment, no other work can proceed. This is the foundation for all subsequent development.

**Independent Test**: Can be fully tested by running `python manage.py runserver` and accessing the Django welcome page at `http://localhost:8000`

**Acceptance Scenarios**:

1. **Given** a fresh clone of the repository, **When** I run the setup commands, **Then** a virtual environment is created with all dependencies installed
2. **Given** Django is installed, **When** I run `python manage.py check`, **Then** the system reports no issues
3. **Given** the project is configured, **When** I run `python manage.py runserver`, **Then** Django starts without errors on port 8000

---

### User Story 2 - Database Connection (Priority: P1)

As a developer, I want PostgreSQL configured and connected so that I can persist data and run migrations.

**Why this priority**: Database connectivity is essential for any Django application. Without it, models cannot be created or tested.

**Independent Test**: Can be fully tested by running `python manage.py migrate` successfully and creating a superuser

**Acceptance Scenarios**:

1. **Given** PostgreSQL is running, **When** Django attempts to connect, **Then** the connection succeeds without errors
2. **Given** the database connection works, **When** I run `python manage.py migrate`, **Then** all initial Django migrations apply successfully
3. **Given** migrations are complete, **When** I run `python manage.py createsuperuser`, **Then** a superuser account is created in the database

---

### User Story 3 - Django Admin Access (Priority: P1)

As a developer, I want to access Django Admin so that I can verify the project is fully functional and ready for model development.

**Why this priority**: Django Admin provides immediate visual confirmation that the entire stack is working correctly.

**Independent Test**: Can be fully tested by logging into `/admin/` with superuser credentials

**Acceptance Scenarios**:

1. **Given** the server is running and superuser exists, **When** I navigate to `/admin/`, **Then** the Django Admin login page appears
2. **Given** I am on the admin login page, **When** I enter valid superuser credentials, **Then** I am logged into Django Admin dashboard

---

### User Story 4 - App Structure Ready (Priority: P2)

As a developer, I want all Django apps created and registered so that I can immediately begin developing models and views.

**Why this priority**: Having apps pre-configured eliminates setup friction when starting feature development.

**Independent Test**: Can be verified by checking `INSTALLED_APPS` and that each app directory exists with proper structure

**Acceptance Scenarios**:

1. **Given** the project is set up, **When** I check the project structure, **Then** apps for core, clients, cases, documents, and users exist
2. **Given** apps are created, **When** I check `settings.py`, **Then** all apps are listed in `INSTALLED_APPS`
3. **Given** apps are registered, **When** I run `python manage.py check`, **Then** no app configuration errors are reported

---

### User Story 5 - Environment Configuration (Priority: P2)

As a developer, I want environment variables properly configured so that sensitive data is not committed to version control.

**Why this priority**: Security best practice requires separation of configuration from code.

**Independent Test**: Can be verified by confirming `.env` is gitignored and `.env.example` documents all required variables

**Acceptance Scenarios**:

1. **Given** the project uses environment variables, **When** I check `.gitignore`, **Then** `.env` is listed and will not be committed
2. **Given** `.env.example` exists, **When** I copy it to `.env`, **Then** all required variables are documented with placeholder values
3. **Given** environment variables are set, **When** Django loads settings, **Then** values are read from `.env` file

---

### Edge Cases

- What happens when PostgreSQL is not running? → Django should fail with a clear connection error message
- What happens when `.env` file is missing? → Application should fail fast with clear error about missing configuration
- What happens when wrong Python version is used? → Requirements should specify Python 3.11+ compatibility

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use Django 5.0.x as the web framework
- **FR-002**: System MUST use PostgreSQL as the database backend
- **FR-003**: System MUST use python-dotenv for environment variable management
- **FR-004**: System MUST include Django REST Framework for API development
- **FR-005**: System MUST include django-cors-headers for cross-origin requests
- **FR-006**: System MUST include django-filter for queryset filtering
- **FR-007**: System MUST include Pillow for image/document handling
- **FR-008**: System MUST have separate Django apps: core, clients, cases, documents, users
- **FR-009**: System MUST configure static files directory at `/static/`
- **FR-010**: System MUST configure media files directory at `/media/`
- **FR-011**: System MUST have a `.gitignore` appropriate for Python/Django projects
- **FR-012**: System MUST have a `.env.example` documenting all required environment variables

### Key Entities

- **Django Project (legaldocs)**: The main Django project container with settings and URL configuration
- **Core App**: Shared utilities, base models with timestamp fields, custom permissions
- **Clients App**: Will contain client/customer management (empty for now)
- **Cases App**: Will contain legal case management (empty for now)
- **Documents App**: Will contain document upload and management (empty for now)
- **Users App**: Will contain custom user model and authentication (empty for now)

## Technical Specification

### Dependencies (requirements.txt)

```
Django==5.0.11
djangorestframework==3.15.2
psycopg2-binary==2.9.10
python-dotenv==1.0.1
Pillow==11.1.0
django-cors-headers==4.6.0
django-filter==24.3
```

### Environment Variables (.env.example)

```
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=legaldocs_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

### Project Structure

```
LegalDocs-Manager/
├── .specify/                    # Spec-kit files (existing)
├── legaldocs/                   # Django project root
│   ├── manage.py
│   ├── legaldocs/               # Project configuration
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── core/                    # Shared utilities app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── clients/                 # Clients app
│   │   └── (standard app files)
│   ├── cases/                   # Cases app
│   │   └── (standard app files)
│   ├── documents/               # Documents app
│   │   └── (standard app files)
│   ├── users/                   # Users app
│   │   └── (standard app files)
│   ├── static/                  # Static files
│   └── media/                   # User uploads
├── .env                         # Environment variables (gitignored)
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── requirements.txt             # Python dependencies
```

### Settings Configuration

Key settings.py modifications:

```python
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    # Local apps
    'core',
    'users',
    'clients',
    'cases',
    'documents',
]

# DRF Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # React/Next.js frontend
]

# Static and Media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## Setup Commands

### 1. Virtual Environment & Dependencies

```bash
# Navigate to project root
cd /home/juanca/proys/LegalDocs-Manager

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Create Django Project & Apps

```bash
# Create Django project
django-admin startproject legaldocs .

# Create apps
python manage.py startapp core
python manage.py startapp users
python manage.py startapp clients
python manage.py startapp cases
python manage.py startapp documents

# Create directories
mkdir -p static media
```

### 3. PostgreSQL Database Setup

```bash
# Connect to PostgreSQL (as postgres user or with sudo)
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE legaldocs_db;
CREATE USER legaldocs_user WITH PASSWORD 'your-secure-password';
ALTER ROLE legaldocs_user SET client_encoding TO 'utf8';
ALTER ROLE legaldocs_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE legaldocs_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE legaldocs_db TO legaldocs_user;
\q
```

### 4. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your actual values
# nano .env  (or use your preferred editor)
```

### 5. Run Migrations & Create Superuser

```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Follow prompts for username, email, password
```

### 6. Verification Commands

```bash
# Check for configuration issues
python manage.py check

# Run development server
python manage.py runserver

# Access in browser:
# - http://localhost:8000/ (Django welcome page)
# - http://localhost:8000/admin/ (Django Admin)
```

### 7. Git Setup

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# First commit (in Spanish per constitution)
git commit -m "feat(proyecto): configuracion inicial de Django con PostgreSQL y DRF

- Crear proyecto Django 'legaldocs' con estructura base
- Configurar PostgreSQL como base de datos
- Instalar dependencias: DRF, corsheaders, django-filter, Pillow
- Crear apps: core, clients, cases, documents, users
- Configurar variables de entorno con python-dotenv
- Agregar .gitignore para Python/Django

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `python manage.py check` returns "System check identified no issues"
- **SC-002**: `python manage.py migrate` completes without errors
- **SC-003**: `python manage.py runserver` starts server on port 8000
- **SC-004**: Django Admin login page loads at `/admin/`
- **SC-005**: Superuser can log into Django Admin successfully
- **SC-006**: All 5 apps (core, clients, cases, documents, users) are listed in admin
- **SC-007**: `.env` file is not tracked by git (verified with `git status`)
- **SC-008**: Project structure matches the defined layout

## Verification Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip list` shows all packages)
- [ ] Django project created at `legaldocs/`
- [ ] All 5 apps created and registered in `INSTALLED_APPS`
- [ ] PostgreSQL database created and accessible
- [ ] `.env` file configured with correct values
- [ ] `.env.example` documents all required variables
- [ ] `.gitignore` includes Python/Django patterns
- [ ] `python manage.py check` passes
- [ ] `python manage.py migrate` succeeds
- [ ] Superuser created
- [ ] Django Admin accessible and functional
- [ ] Development server runs without errors
- [ ] Initial git commit created
