from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
        ('civil', _('Civil')),
        ('penal', _('Penal')),
        ('laboral', _('Laboral')),
        ('mercantil', _('Mercantil')),
        ('familia', _('Familia')),
    ]

    STATUS_CHOICES = [
        ('en_proceso', _('En Proceso')),
        ('pendiente_documentos', _('Pendiente Documentos')),
        ('en_revision', _('En Revisión')),
        ('cerrado', _('Cerrado')),
    ]

    PRIORITY_CHOICES = [
        ('baja', _('Baja')),
        ('media', _('Media')),
        ('alta', _('Alta')),
        ('urgente', _('Urgente')),
    ]

    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.PROTECT,
        related_name='cases',
        verbose_name=_("Cliente")
    )
    case_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name=_("Número de caso")
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_("Título")
    )
    description = models.TextField(
        verbose_name=_("Descripción")
    )
    case_type = models.CharField(
        max_length=20,
        choices=CASE_TYPE_CHOICES,
        verbose_name=_("Tipo de caso")
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='en_proceso',
        verbose_name=_("Estado")
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='media',
        verbose_name=_("Prioridad")
    )
    start_date = models.DateField(
        verbose_name=_("Fecha de inicio")
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Fecha límite")
    )
    closed_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Fecha de cierre")
    )
    assigned_to = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cases',
        verbose_name=_("Asignado a")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de creación")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Última actualización")
    )

    objects = CaseManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Caso")
        verbose_name_plural = _("Casos")
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
