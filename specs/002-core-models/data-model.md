# Data Model: Core Entities

**Feature**: 002-core-models | **Date**: 2026-01-16

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LegalDocs Manager ERD                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐         ┌─────────────────────────┐
│       auth.User     │         │         Client          │
├─────────────────────┤         ├─────────────────────────┤
│ PK id               │         │ PK id                   │
│    username         │         │    full_name            │
│    email            │         │ UK identification_number│
│    password         │         │    email                │
│    ...              │         │    phone                │
└─────────────────────┘         │    address              │
         │                      │    created_at           │
         │                      │    updated_at           │
         │ SET_NULL             │    is_active            │
         │ (assigned_to)        │    notes                │
         ▼                      └─────────────────────────┘
┌─────────────────────────────────────┐          │
│              Case                    │          │
├─────────────────────────────────────┤          │ PROTECT
│ PK id                               │          │ (client)
│ UK case_number (auto-generated)     │◄─────────┘
│ FK client_id ──────────────────────►│
│ FK assigned_to_id (nullable)        │
│    title                            │
│    description                      │
│    case_type [civil|penal|...]      │
│    status [en_proceso|...]          │
│    priority [baja|media|alta|...]   │
│    start_date                       │
│    deadline (nullable)              │
│    closed_date (nullable)           │
│    created_at                       │
│    updated_at                       │
└─────────────────────────────────────┘
         │
         │ CASCADE
         │ (case)
         ▼
┌─────────────────────────────────────┐
│            Document                  │
├─────────────────────────────────────┤
│ PK id                               │
│ FK case_id ─────────────────────────┤
│ FK uploaded_by_id (nullable)        │
│    document_type [contrato|...]     │
│    title                            │
│    description                      │
│    file (FileField)                 │
│    file_size (auto-calculated)      │
│    uploaded_at                      │
│    is_confidential                  │
└─────────────────────────────────────┘
         │
         │ SET_NULL
         │ (uploaded_by)
         ▼
┌─────────────────────┐
│       auth.User     │
└─────────────────────┘
```

## Relationship Summary

| From | To | Cardinality | on_delete | related_name |
|------|----|-------------|-----------|--------------|
| Case | Client | Many-to-One | PROTECT | cases |
| Case | User | Many-to-One | SET_NULL | assigned_cases |
| Document | Case | Many-to-One | CASCADE | documents |
| Document | User | Many-to-One | SET_NULL | uploaded_documents |

## Entity Details

### Client

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Primary key |
| full_name | CharField(200) | Required | Nombre completo |
| identification_number | CharField(50) | Unique, Required | Número de identificación |
| email | EmailField | Required | Correo electrónico |
| phone | CharField(20) | Required | Teléfono |
| address | TextField | Optional | Dirección |
| created_at | DateTimeField | Auto | Fecha de creación |
| updated_at | DateTimeField | Auto | Última actualización |
| is_active | BooleanField | Default=True | Estado activo |
| notes | TextField | Optional | Notas adicionales |

**Ordering**: `-created_at` (newest first)

### Case

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Primary key |
| client | ForeignKey | Required, PROTECT | Cliente asociado |
| case_number | CharField(20) | Unique, Auto, ReadOnly | Número de caso |
| title | CharField(200) | Required | Título del caso |
| description | TextField | Required | Descripción |
| case_type | CharField(20) | Choices | Tipo de caso |
| status | CharField(30) | Choices, Default='en_proceso' | Estado |
| priority | CharField(20) | Choices, Default='media' | Prioridad |
| start_date | DateField | Required | Fecha de inicio |
| deadline | DateField | Optional | Fecha límite |
| closed_date | DateField | Optional | Fecha de cierre |
| assigned_to | ForeignKey | Optional, SET_NULL | Usuario asignado |
| created_at | DateTimeField | Auto | Fecha de creación |
| updated_at | DateTimeField | Auto | Última actualización |

**Ordering**: `-created_at` (newest first)

**Case Type Choices**:
- `civil` → Civil
- `penal` → Penal
- `laboral` → Laboral
- `mercantil` → Mercantil
- `familia` → Familia

**Status Choices**:
- `en_proceso` → En Proceso
- `pendiente_documentos` → Pendiente Documentos
- `en_revision` → En Revisión
- `cerrado` → Cerrado

**Priority Choices**:
- `baja` → Baja
- `media` → Media
- `alta` → Alta
- `urgente` → Urgente

### Document

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Primary key |
| case | ForeignKey | Required, CASCADE | Caso asociado |
| document_type | CharField(20) | Choices | Tipo de documento |
| title | CharField(200) | Required | Título |
| description | TextField | Optional | Descripción |
| file | FileField | Required | Archivo |
| file_size | IntegerField | Auto, ReadOnly | Tamaño en bytes |
| uploaded_by | ForeignKey | Optional, SET_NULL | Usuario que subió |
| uploaded_at | DateTimeField | Auto | Fecha de subida |
| is_confidential | BooleanField | Default=False | Confidencial |

**Ordering**: `-uploaded_at` (newest first)

**Document Type Choices**:
- `contrato` → Contrato
- `demanda` → Demanda
- `poder` → Poder
- `sentencia` → Sentencia
- `escritura` → Escritura
- `otro` → Otro

## Access Patterns

### Common Queries

```python
# Get all cases for a client
client.cases.all()

# Get all documents for a case
case.documents.all()

# Get active (non-closed) cases
Case.objects.active()

# Get cases by status
Case.objects.by_status('en_proceso')

# Get cases assigned to a user
user.assigned_cases.all()

# Get documents uploaded by a user
user.uploaded_documents.all()
```

### Business Rules

1. **Client Deletion Protection**: Cannot delete a client that has cases (raises ProtectedError)
2. **Cascade Document Deletion**: Deleting a case automatically deletes all its documents
3. **Auto Case Number**: Case numbers are automatically generated on first save
4. **Auto File Size**: Document file size is calculated automatically on save
5. **Default Status**: New cases default to 'en_proceso' status
6. **Default Priority**: New cases default to 'media' priority
