from django.db import models


class Document(models.Model):
    """
    Represents an uploaded document linked to a legal case.

    Stores document metadata including type, file reference,
    and upload information. Documents are automatically deleted
    when their associated case is deleted (CASCADE).
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
    title = models.CharField(
        max_length=200,
        verbose_name="Título"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
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
        blank=True,
        related_name='uploaded_documents',
        verbose_name="Subido por"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de subida"
    )
    is_confidential = models.BooleanField(
        default=False,
        verbose_name="Confidencial"
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self) -> str:
        return f"{self.get_document_type_display()}: {self.title}"

    def save(self, *args, **kwargs):
        """
        Override save to auto-calculate file_size from uploaded file.
        """
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
