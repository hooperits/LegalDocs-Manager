# LegalDocs Manager Constitution

## Core Principles

### I. Django Best Practices First
All code must adhere to Django's established conventions and idioms. Follow the "Django way" for solving problems rather than inventing custom patterns. Use Django's built-in features (ORM, forms, validators, permissions) before reaching for third-party solutions. Code should be recognizable and maintainable by any Django developer.

### II. Clean Architecture & Separation of Concerns
- **App-per-domain**: Each Django app owns a single domain (clients, cases, documents, users, core)
- **Core app**: Shared utilities, base classes, and cross-cutting concerns live in `core/`
- **No circular imports**: Apps may only import from `core/` or Django itself, never from sibling apps at the model level
- **Fat models, thin views**: Business logic belongs in models and services, not in views

### III. API-First Design
Every feature must be accessible via RESTful API using Django REST Framework:
- Proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Meaningful HTTP status codes
- Consistent response formats with serializers
- Token-based authentication for all protected endpoints
- Pagination, filtering, and search on list endpoints

### IV. Documentation is Mandatory
- **Docstrings**: Every class, method, and function must have a docstring explaining its purpose
- **Type hints**: Use Python type hints for function signatures
- **API documentation**: All endpoints documented via DRF's built-in schema generation
- **Code comments**: Only for complex logic that isn't self-evident

### V. Security by Default
- Never commit secrets, credentials, or API keys
- Use environment variables for all sensitive configuration
- Validate all user input at API boundaries
- Use Django's built-in protections (CSRF, XSS, SQL injection prevention)
- Implement proper permission checks on all views
- File uploads must be validated for type and size

## Technical Standards

### Technology Stack
- **Python**: 3.11+ (use modern syntax and features)
- **Django**: 5.x with latest security patches
- **Database**: PostgreSQL 15+ (use Django ORM, avoid raw SQL)
- **API**: Django REST Framework 3.15+
- **Authentication**: DRF TokenAuthentication

### Code Style
- Follow PEP 8 with 88-character line length (Black formatter compatible)
- Use `snake_case` for functions/variables, `PascalCase` for classes
- Imports ordered: stdlib, third-party, Django, local apps
- Prefer class-based views (APIView, generics, viewsets) over function-based
- Use Django's `Q` objects for complex queries

### Model Conventions
- All models inherit from a base model in `core/` with `created_at` and `updated_at`
- Use `ForeignKey` with explicit `on_delete` behavior
- Add `related_name` to all relationship fields
- Include `__str__` method on all models
- Use `Meta` class for ordering, verbose names, and constraints
- Validate at the model level with `clean()` and validators

### Database Practices
- One migration per logical change
- Never edit existing migrations in production
- Use `select_related` and `prefetch_related` to avoid N+1 queries
- Add database indexes for frequently queried fields

## Development Workflow

### Commit Standards
- Commit messages must be written in **Spanish**
- Use conventional commit format: `tipo(alcance): descripcion`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Example: `feat(clientes): agregar endpoint para listar clientes activos`

### Development Sequence
1. **Models first**: Define data structures and relationships
2. **Migrations**: Generate and review migrations
3. **Admin**: Register models and customize admin interface
4. **Serializers**: Create DRF serializers
5. **Views**: Implement API endpoints
6. **URLs**: Wire up routing
7. **Test**: Verify functionality works

### Testing Requirements
- Test each component before moving to the next
- Use Django's TestCase for model and integration tests
- Use DRF's APITestCase for endpoint tests
- Create fixtures for demo data in `fixtures/` directory

### Environment Configuration
- Use `python-decouple` or `django-environ` for environment variables
- Required env vars: `SECRET_KEY`, `DATABASE_URL`, `DEBUG`, `ALLOWED_HOSTS`
- Never use default secrets in any environment
- Maintain `requirements.txt` with pinned versions

## Project Structure

```
legaldocs_manager/
├── manage.py
├── requirements.txt
├── .env.example
├── config/                 # Project settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # Shared utilities
│   ├── models.py          # Base models
│   ├── permissions.py     # Custom permissions
│   └── utils.py
├── users/                  # User management
├── clients/                # Client management
├── cases/                  # Legal cases
├── documents/              # Document handling
└── fixtures/               # Demo data
```

## Governance

This constitution defines the non-negotiable standards for LegalDocs Manager. All code contributions must comply with these principles. When in doubt:

1. Consult Django's official documentation
2. Follow the principle of least surprise
3. Prioritize readability over cleverness
4. Keep the POC scope focused - avoid feature creep

**Exceptions**: Any deviation from this constitution must be documented with justification in the code or commit message.

**Version**: 1.0.0 | **Ratified**: 2026-01-16 | **Last Amended**: 2026-01-16
