from django.db import models
from django.utils import timezone


class CaseManager(models.Manager):
    """
    Custom manager for Case model with status filtering.

    Provides convenience methods for common case queries
    such as filtering by status or getting active cases.
    """

    def active(self):
        """
        Return cases that are not closed.

        Returns:
            QuerySet: Cases with status other than 'cerrado'.
        """
        return self.exclude(status='cerrado')

    def by_status(self, status: str):
        """
        Filter cases by status.

        Args:
            status: The status value to filter by.

        Returns:
            QuerySet: Cases matching the given status.
        """
        return self.filter(status=status)


class Case(models.Model):
    """
    Represents a legal case/matter linked to a client.

    Tracks legal cases with auto-generated case numbers,
    status management, priority levels, and key dates.
    Cases are protected from deletion while associated with clients.
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
    title = models.CharField(
        max_length=200,
        verbose_name="Título"
    )
    description = models.TextField(
        verbose_name="Descripción"
    )
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
    start_date = models.DateField(
        verbose_name="Fecha de inicio"
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha límite"
    )
    closed_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de cierre"
    )
    assigned_to = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cases',
        verbose_name="Asignado a"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    objects = CaseManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Caso"
        verbose_name_plural = "Casos"
        indexes = [
            models.Index(fields=['client'], name='case_client_idx'),
            models.Index(fields=['status'], name='case_status_idx'),
            models.Index(fields=['case_type'], name='case_type_idx'),
            models.Index(fields=['-created_at'], name='case_created_idx'),
        ]

    def __str__(self) -> str:
        return f"{self.case_number} - {self.title}"

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate case_number if not set.
        """
        if not self.case_number:
            self.case_number = self.generate_case_number()
        super().save(*args, **kwargs)

    @classmethod
    def generate_case_number(cls) -> str:
        """
        Generate unique case number in format CASE-YYYY-NNNN.

        Queries for the last case number of the current year
        and increments the sequential number.

        Returns:
            str: A unique case number like 'CASE-2026-0001'.
        """
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
