# LegalDocs Manager - Demo Script

## Overview

This 5-minute demo showcases the key features of LegalDocs Manager, a REST API for managing legal documents, clients, and cases.

## Prerequisites

1. Start the development server:
   ```bash
   cd legaldocs
   python manage.py runserver
   ```

2. Have the Postman collection imported, or use curl commands below.

---

## Demo Flow (5 minutes)

### 1. Authentication (1 minute)

**Register a new user:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo_user",
    "email": "demo@example.com",
    "password": "Demo123456",
    "password_confirm": "Demo123456"
  }'
```

**Login to get token:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "demo_user", "password": "Demo123456"}'
```

Save the returned token for subsequent requests.

---

### 2. Create a Client (1 minute)

```bash
curl -X POST http://localhost:8000/api/v1/clients/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan Carlos Pérez",
    "identification_number": "CC-12345678",
    "email": "juan.perez@email.com",
    "phone": "+57 300 123 4567",
    "address": "Calle 123 #45-67, Bogotá"
  }'
```

**Key points:**
- All fields are validated
- Identification number must be unique
- Spanish field names in error messages

---

### 3. Create a Case (1 minute)

```bash
curl -X POST http://localhost:8000/api/v1/cases/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "client": 1,
    "title": "Demanda laboral - Despido injustificado",
    "description": "El cliente fue despedido sin justa causa después de 5 años de servicio.",
    "case_type": "laboral",
    "status": "en_proceso",
    "priority": "alta",
    "start_date": "2026-01-15",
    "deadline": "2026-03-15"
  }'
```

**Key points:**
- Auto-generated case number (CASE-2026-0001)
- Multiple case types: civil, penal, laboral, mercantil, familia
- Priority levels: baja, media, alta, urgente

---

### 4. Upload a Document (1 minute)

```bash
curl -X POST http://localhost:8000/api/v1/documents/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "case=1" \
  -F "title=Contrato de trabajo original" \
  -F "document_type=contrato" \
  -F "description=Contrato firmado el 01/01/2021" \
  -F "file=@/path/to/document.pdf"
```

**Key points:**
- Supported file types: PDF, DOC, DOCX, TXT, JPG, PNG
- Maximum file size: 10MB
- File type validation using magic bytes (not just extension)

---

### 5. Dashboard & Search (1 minute)

**View dashboard statistics:**
```bash
curl -X GET http://localhost:8000/api/v1/dashboard/ \
  -H "Authorization: Token YOUR_TOKEN"
```

Shows:
- Total clients and active clients
- Cases by status and type
- Recent cases
- Upcoming deadlines

**Search across all data:**
```bash
curl -X GET "http://localhost:8000/api/v1/search/?q=Juan" \
  -H "Authorization: Token YOUR_TOKEN"
```

Searches clients, cases, and documents simultaneously.

---

## Security Features to Highlight

1. **Rate Limiting**: Login/register limited to 5 requests per minute
2. **File Validation**: Validates actual file content, not just extension
3. **Token Authentication**: Secure token-based authentication
4. **CORS Protection**: Configured allowed origins

---

## API Documentation

Full API documentation available at:
- Swagger UI: http://localhost:8000/api/v1/docs/
- ReDoc: http://localhost:8000/api/v1/redoc/

---

## End of Demo

Thank you for watching the LegalDocs Manager demo!

For questions or issues, please check the repository README or open an issue.
