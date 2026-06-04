from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    """
    Represents a legal client with contact information.

    Stores personal and contact details for individuals or entities
    that engage legal services. Clients are the foundation entity
    that cases and documents are associated with.
    """

    full_name = models.CharField(
        max_length=200,
        verbose_name=_("Nombre completo")
    )
    identification_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Número de identificación")
    )
    email = models.EmailField(
        verbose_name=_("Correo electrónico")
    )
    phone = models.CharField(
        max_length=20,
        verbose_name=_("Teléfono")
    )
    address = models.TextField(
        blank=True,
        verbose_name=_("Dirección")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de creación")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Última actualización")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Activo")
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notas")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")

    def __str__(self) -> str:
        return f"{self.full_name} ({self.identification_number})"
