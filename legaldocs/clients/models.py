from django.db import models


class Client(models.Model):
    """
    Represents a legal client with contact information.

    Stores personal and contact details for individuals or entities
    that engage legal services. Clients are the foundation entity
    that cases and documents are associated with.
    """

    full_name = models.CharField(
        max_length=200,
        verbose_name="Nombre completo"
    )
    identification_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número de identificación"
    )
    email = models.EmailField(
        verbose_name="Correo electrónico"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Teléfono"
    )
    address = models.TextField(
        blank=True,
        verbose_name="Dirección"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notas"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self) -> str:
        return f"{self.full_name} ({self.identification_number})"
