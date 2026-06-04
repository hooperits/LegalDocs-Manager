from django.db import models
from django.utils.translation import gettext_lazy as _


class Document(models.Model):
    """
    Represents an uploaded document linked to a legal case.

    Stores document metadata including type, file reference,
    and upload information. Documents are automatically deleted
    when their associated case is deleted (CASCADE).
    """

    DOCUMENT_TYPE_CHOICES = [
        ('contrato', _('Contrato')),
        ('demanda', _('Demanda')),
        ('poder', _('Poder')),
        ('sentencia', _('Sentencia')),
        ('escritura', _('Escritura')),
        ('otro', _('Otro')),
    ]

    case = models.ForeignKey(
        'cases.Case',
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_("Caso")
    )
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name=_("Tipo de documento")
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_("Título")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Descripción")
    )
    file = models.FileField(
        upload_to='legal_documents/',
        verbose_name=_("Archivo")
    )
    file_size = models.IntegerField(
        editable=False,
        verbose_name=_("Tamaño del archivo (bytes)")
    )
    uploaded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_documents',
        verbose_name=_("Subido por")
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de subida")
    )
    is_confidential = models.BooleanField(
        default=False,
        verbose_name=_("Confidencial")
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = _("Documento")
        verbose_name_plural = _("Documentos")
        indexes = [
            models.Index(fields=['case'], name='doc_case_idx'),
            models.Index(fields=['-uploaded_at'], name='doc_uploaded_idx'),
            models.Index(fields=['document_type'], name='doc_type_idx'),
        ]

    def __str__(self) -> str:
        return f"{self.get_document_type_display()}: {self.title}"

    def save(self, *args, **kwargs):
        """
        Override save to auto-calculate file_size from uploaded file.
        """
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
