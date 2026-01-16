# Feature Specification: Core Data Models

**Feature Branch**: `002-core-models`
**Created**: 2026-01-16
**Status**: Draft
**Input**: Define Django models for Client, Case, and Document entities with relationships, validation, and fixtures

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Client Management Data (Priority: P1)

As a legal staff member, I want to store client information so that I can manage client records and associate them with legal cases.

**Why this priority**: Clients are the foundation of the system - cases and documents depend on having clients first.

**Independent Test**: Can be fully tested by creating, reading, updating, and deleting clients via Django Admin and verifying data integrity.

**Acceptance Scenarios**:

1. **Given** the database is set up, **When** I create a new client with required fields, **Then** the client is saved with auto-generated timestamps
2. **Given** a client exists, **When** I try to create another client with the same identification_number, **Then** the system rejects it as duplicate
3. **Given** clients exist, **When** I query active clients, **Then** only clients with is_active=True are returned
4. **Given** a client exists, **When** I view their __str__ representation, **Then** I see their full name and identification number

---

### User Story 2 - Case Management Data (Priority: P1)

As a lawyer, I want to create and track legal cases so that I can manage ongoing legal matters for my clients.

**Why this priority**: Cases are the core business entity that links clients to documents and tracks legal work.

**Independent Test**: Can be fully tested by creating cases with auto-generated case numbers and verifying status filtering works.

**Acceptance Scenarios**:

1. **Given** a client exists, **When** I create a new case, **Then** a unique case_number is auto-generated in format CASE-YYYY-NNNN
2. **Given** cases exist with different statuses, **When** I filter by status "En Proceso", **Then** only matching cases are returned
3. **Given** a case exists, **When** I view its __str__ representation, **Then** I see the case number and title
4. **Given** multiple cases exist, **When** I query all cases, **Then** they are ordered by creation date descending

---

### User Story 3 - Document Management Data (Priority: P1)

As a legal assistant, I want to upload and categorize documents so that all case-related files are organized and accessible.

**Why this priority**: Documents are essential deliverables in legal work and must be properly linked to cases.

**Independent Test**: Can be fully tested by uploading documents, verifying file size calculation, and checking case association.

**Acceptance Scenarios**:

1. **Given** a case exists, **When** I upload a document, **Then** the file is saved to 'legal_documents/' and file_size is auto-calculated
2. **Given** a document exists, **When** I view its __str__ representation, **Then** I see the document type and title
3. **Given** documents exist for a case, **When** I access case.documents, **Then** I get all related documents via related_name

---

### User Story 4 - Sample Data for Testing (Priority: P2)

As a developer, I want fixture data so that I can test the system with realistic sample data.

**Why this priority**: Fixtures enable rapid testing and demonstration of the system.

**Independent Test**: Can be verified by loading fixtures and confirming 5 clients, 10 cases, and 15 documents exist.

**Acceptance Scenarios**:

1. **Given** an empty database, **When** I run loaddata command, **Then** 5 clients, 10 cases, and 15 documents are created
2. **Given** fixtures are loaded, **When** I view Django Admin, **Then** all sample data is visible and properly related

---

### Edge Cases

- What happens when deleting a client with cases? → Cases should be protected (PROTECT) or cascade based on business rules
- What happens when deleting a case with documents? → Documents should cascade delete with the case
- What happens when uploading a very large file? → File size should be calculated correctly
- What happens with invalid case_type or status? → Model validation should reject invalid choices

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST store client information with unique identification numbers
- **FR-002**: System MUST auto-generate unique case numbers in format CASE-YYYY-NNNN
- **FR-003**: System MUST track case status with predefined choices
- **FR-004**: System MUST store uploaded documents linked to cases
- **FR-005**: System MUST auto-calculate document file sizes
- **FR-006**: System MUST enforce referential integrity between models
- **FR-007**: System MUST provide custom manager for filtering cases by status
- **FR-008**: System MUST include meaningful __str__ methods for all models
- **FR-009**: System MUST order models appropriately by default (Meta ordering)
- **FR-010**: System MUST include fixtures with sample data for testing

### Key Entities

- **Client**: Legal client with contact information and identification
- **Case**: Legal matter/case linked to a client with status tracking
- **Document**: Uploaded file linked to a case with metadata

## Technical Specification

### Client Model (clients/models.py)

```python
class Client(models.Model):
    """
    Represents a legal client with contact information.
    """
    full_name = models.CharField(max_length=200, verbose_name="Nombre completo")
    identification_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número de identificación"
    )
    email = models.EmailField(verbose_name="Correo electrónico")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    address = models.TextField(blank=True, verbose_name="Dirección")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    notes = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.full_name} ({self.identification_number})"
```

### Case Model (cases/models.py)

```python
class CaseManager(models.Manager):
    """Custom manager for Case model with status filtering."""

    def active(self):
        """Return cases that are not closed."""
        return self.exclude(status='cerrado')

    def by_status(self, status):
        """Filter cases by status."""
        return self.filter(status=status)


class Case(models.Model):
    """
    Represents a legal case/matter linked to a client.
    """
    CASE_TYPE_CHOICES = [
        ('civil', 'Civil'),
        ('penal', 'Penal'),
        ('laboral', 'Laboral'),
        ('mercantil', 'Mercantil'),
        ('familia', 'Familia'),
    ]

    STATUS_CHOICES = [
        ('en_proceso', 'En Proceso'),
        ('pendiente_documentos', 'Pendiente Documentos'),
        ('en_revision', 'En Revisión'),
        ('cerrado', 'Cerrado'),
    ]

    PRIORITY_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.PROTECT,
        related_name='cases',
        verbose_name="Cliente"
    )
    case_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name="Número de caso"
    )
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    case_type = models.CharField(
        max_length=20,
        choices=CASE_TYPE_CHOICES,
        verbose_name="Tipo de caso"
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='en_proceso',
        verbose_name="Estado"
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='media',
        verbose_name="Prioridad"
    )
    start_date = models.DateField(verbose_name="Fecha de inicio")
    deadline = models.DateField(null=True, blank=True, verbose_name="Fecha límite")
    closed_date = models.DateField(null=True, blank=True, verbose_name="Fecha de cierre")
    assigned_to = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cases',
        verbose_name="Asignado a"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CaseManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Caso"
        verbose_name_plural = "Casos"

    def __str__(self):
        return f"{self.case_number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.case_number:
            self.case_number = self.generate_case_number()
        super().save(*args, **kwargs)

    @classmethod
    def generate_case_number(cls):
        """
        Generate unique case number in format CASE-YYYY-NNNN.
        """
        from django.utils import timezone
        year = timezone.now().year
        prefix = f"CASE-{year}-"

        last_case = cls.objects.filter(
            case_number__startswith=prefix
        ).order_by('-case_number').first()

        if last_case:
            last_number = int(last_case.case_number.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"{prefix}{new_number:04d}"
```

### Document Model (documents/models.py)

```python
class Document(models.Model):
    """
    Represents an uploaded document linked to a legal case.
    """
    DOCUMENT_TYPE_CHOICES = [
        ('contrato', 'Contrato'),
        ('demanda', 'Demanda'),
        ('poder', 'Poder'),
        ('sentencia', 'Sentencia'),
        ('escritura', 'Escritura'),
        ('otro', 'Otro'),
    ]

    case = models.ForeignKey(
        'cases.Case',
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name="Caso"
    )
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name="Tipo de documento"
    )
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descripción")
    file = models.FileField(
        upload_to='legal_documents/',
        verbose_name="Archivo"
    )
    file_size = models.IntegerField(
        editable=False,
        verbose_name="Tamaño del archivo (bytes)"
    )
    uploaded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        verbose_name="Subido por"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_confidential = models.BooleanField(
        default=False,
        verbose_name="Confidencial"
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return f"{self.get_document_type_display()}: {self.title}"

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
```

### Fixtures Structure

```
legaldocs/fixtures/
├── clients.json      # 5 sample clients
├── cases.json        # 10 sample cases
└── documents.json    # 15 sample documents
```

### Sample Fixture Data (clients.json)

```json
[
  {
    "model": "clients.client",
    "pk": 1,
    "fields": {
      "full_name": "María García López",
      "identification_number": "12345678A",
      "email": "maria.garcia@email.com",
      "phone": "+34 612 345 678",
      "address": "Calle Mayor 123, Madrid",
      "is_active": true,
      "notes": "Cliente preferente"
    }
  }
]
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All three models (Client, Case, Document) are created with specified fields
- **SC-002**: `python manage.py makemigrations` generates migrations without errors
- **SC-003**: `python manage.py migrate` applies migrations successfully
- **SC-004**: Case.generate_case_number() produces format CASE-YYYY-NNNN
- **SC-005**: Case.objects.by_status('en_proceso') returns filtered queryset
- **SC-006**: Document.save() auto-calculates file_size from uploaded file
- **SC-007**: `python manage.py loaddata` loads all fixtures successfully
- **SC-008**: Django Admin displays all models with proper field configuration
- **SC-009**: ForeignKey relationships work correctly with related_name access
- **SC-010**: Deleting a client with cases raises ProtectedError

## Verification Checklist

- [ ] Client model created with all specified fields
- [ ] Case model created with all specified fields and choices
- [ ] Document model created with all specified fields
- [ ] CaseManager implemented with active() and by_status() methods
- [ ] Case.generate_case_number() method works correctly
- [ ] Document.save() calculates file_size automatically
- [ ] All models have __str__ methods
- [ ] All models have Meta class with ordering
- [ ] All ForeignKeys have related_name
- [ ] Migrations created and applied
- [ ] Fixtures created (5 clients, 10 cases, 15 documents)
- [ ] Fixtures load without errors
- [ ] Models registered in Django Admin
- [ ] Admin displays models with proper list_display
