# LegalDocs Manager

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.15-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Coverage](https://img.shields.io/badge/Coverage-98%25-brightgreen.svg)
![Tests](https://img.shields.io/badge/Tests-163%20passing-brightgreen.svg)

A comprehensive legal document management system built with Django REST Framework. Designed to help law firms and legal professionals manage clients, cases, and documents efficiently.

## Features

- **Client Management**: Track client information, contact details, and associated cases
- **Case Management**: Handle legal cases with status tracking, priorities, and automatic case number generation
- **Document Management**: Upload, organize, and manage legal documents with confidentiality controls
- **Dashboard**: Real-time statistics and overview of active cases
- **Search**: Global search across clients, cases, and documents
- **User Authentication**: Token-based authentication with registration, login, and profile management
- **API Documentation**: Interactive Swagger UI documentation

## Screenshots

### Swagger API Documentation

The API is fully documented with interactive Swagger UI:

![Swagger Overview](docs/screenshots/07-api/01-swagger-overview.png)

### Authentication Endpoints

Secure token-based authentication with login and registration:

![Login Endpoint](docs/screenshots/01-auth/02-login-endpoint.png)

### Client Management

Complete CRUD operations for managing legal clients:

![Client List](docs/screenshots/02-clients/02-client-list-endpoint.png)

### Case Management

Track legal cases with status, priority, and filtering:

![Case List](docs/screenshots/03-cases/02-case-list-filters.png)

![Case Statistics](docs/screenshots/03-cases/04-case-statistics-endpoint.png)

### Document Management

Upload and manage legal documents with file validation:

![Document Upload](docs/screenshots/04-documents/03-document-upload-endpoint.png)

### Dashboard & Search

Real-time statistics and global search functionality:

![Dashboard](docs/screenshots/05-dashboard/01-dashboard-endpoint.png)

### Django Admin Interface

Powerful admin interface for advanced management:

![Admin Dashboard](docs/screenshots/06-admin/02-admin-dashboard.png)

![Admin Cases](docs/screenshots/06-admin/04-admin-cases-list.png)

> 📸 **[View all screenshots →](docs/screenshots/README.md)**

## Tech Stack

- **Backend**: Python 3.11+, Django 5.x, Django REST Framework 3.15+
- **Database**: PostgreSQL 15+ (SQLite for development/testing)
- **Authentication**: Token Authentication (DRF)
- **API Documentation**: drf-spectacular (OpenAPI 3.0)
- **Testing**: Django TestCase, DRF APITestCase, coverage.py

## Installation

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15+ (optional, SQLite works for development)
- pip (Python package manager)

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd LegalDocs-Manager
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy the example environment file and configure it:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your settings (see [Environment Variables](#environment-variables) below).

5. **Run database migrations**

   ```bash
   cd legaldocs
   python manage.py migrate
   ```

6. **Create a superuser** (optional)

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/api/v1/`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required in production |
| `DEBUG` | Enable debug mode | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` |
| `DB_NAME` | Database name | `legaldocs_db` |
| `DB_USER` | Database user | `legaldocs_user` |
| `DB_PASSWORD` | Database password | Required |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |

### Example .env file

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=legaldocs_db
DB_USER=legaldocs_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## Database Setup

### PostgreSQL (Production)

1. **Install PostgreSQL**

   ```bash
   # Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib

   # macOS with Homebrew
   brew install postgresql
   ```

2. **Create database and user**

   ```sql
   CREATE DATABASE legaldocs_db;
   CREATE USER legaldocs_user WITH PASSWORD 'your-password';
   ALTER ROLE legaldocs_user SET client_encoding TO 'utf8';
   ALTER ROLE legaldocs_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE legaldocs_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE legaldocs_db TO legaldocs_user;
   ```

### SQLite (Development)

SQLite is automatically used during tests. For local development with SQLite, modify `settings.py` or set environment variables accordingly.

## Running Tests

Run the full test suite:

```bash
cd legaldocs
python manage.py test
```

Run tests for specific apps:

```bash
python manage.py test clients cases documents
```

Run tests with verbose output:

```bash
python manage.py test --verbosity=2
```

### Test Coverage

Run tests with coverage report:

```bash
coverage run --source='clients,cases,documents,api' manage.py test
coverage report
coverage html  # Generate HTML report in htmlcov/
```

Current coverage target: **70%+**

## Demo Data

Load demo data with realistic legal scenarios:

```bash
python manage.py load_demo_data
```

This creates:
- 20+ clients with Spanish names
- 30+ legal cases across different types
- 50+ documents

To clear and reload demo data:

```bash
python manage.py load_demo_data --clear
```

## API Overview

All endpoints are prefixed with `/api/v1/`

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register/` | POST | Register new user |
| `/api/v1/auth/login/` | POST | Login and get token |
| `/api/v1/auth/logout/` | POST | Logout and invalidate token |
| `/api/v1/auth/me/` | GET | Get current user info |

### Clients

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/clients/` | GET | List all clients |
| `/api/v1/clients/` | POST | Create a client |
| `/api/v1/clients/{id}/` | GET | Get client details |
| `/api/v1/clients/{id}/` | PUT/PATCH | Update client |
| `/api/v1/clients/{id}/` | DELETE | Delete client |
| `/api/v1/clients/{id}/cases/` | GET | Get client's cases |

### Cases

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/cases/` | GET | List all cases |
| `/api/v1/cases/` | POST | Create a case |
| `/api/v1/cases/{id}/` | GET | Get case details |
| `/api/v1/cases/{id}/` | PUT/PATCH | Update case |
| `/api/v1/cases/{id}/` | DELETE | Delete case |
| `/api/v1/cases/{id}/close/` | POST | Close a case |
| `/api/v1/cases/statistics/` | GET | Get case statistics |

### Documents

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/documents/` | GET | List all documents |
| `/api/v1/documents/` | POST | Upload a document |
| `/api/v1/documents/{id}/` | GET | Get document details |
| `/api/v1/documents/{id}/` | PUT/PATCH | Update document |
| `/api/v1/documents/{id}/` | DELETE | Delete document |

### Other Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/dashboard/` | GET | Dashboard statistics |
| `/api/v1/search/` | GET | Global search |
| `/api/v1/profile/` | GET/PATCH | User profile |

### API Documentation

- **OpenAPI Schema**: `/api/v1/schema/`
- **Swagger UI**: `/api/v1/docs/`

## Project Structure

```
LegalDocs-Manager/
├── legaldocs/
│   ├── api/              # API views, authentication, permissions
│   ├── cases/            # Case model, views, serializers
│   ├── clients/          # Client model, views, serializers
│   ├── core/             # Core utilities, management commands
│   ├── documents/        # Document model, views, serializers
│   ├── fixtures/         # Demo data fixtures
│   ├── legaldocs/        # Django settings
│   └── manage.py
├── specs/                # Feature specifications
├── requirements.txt
├── README.md
├── API_DOCS.md          # Detailed API documentation
└── DEPLOYMENT.md        # Production deployment guide
```

## Contributing

1. Create a feature branch from `master`
2. Write tests for new functionality
3. Ensure all tests pass with 70%+ coverage
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
