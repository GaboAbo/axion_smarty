"""
Models for the AuthUser app.

Includes custom user models for Engineers and Clients who are associated with entities.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class EnterpriseUser(models.Model):
    """
    Abstract base model for users belonging to an entity (company or institution).

    Attributes:
        entity (Entity): The entity (organization) the user is associated with.
        role (str): The user's role within the entity, chosen from predefined choices.
    """

    ROLE_CHOICES = [
        ("MAN", "Gerente"),
        ("ENG", "Ingeniero/a"),
        ("REP", "Representante de ventas"),
        ("ADM", "Administrativo"),
        ("BOS", "Jefe/a de unidad"),
        ("SUP", "Supervisor/a"),
        ("DOC", "Doctor/a"),
        ("NUR", "Enfermero/a"),
        ("TEN", "Tens"),
    ]

    entity = models.ForeignKey(
        "Entity.Entity",
        verbose_name="Entidad",
        on_delete=models.CASCADE
    )
    role = models.CharField(
        "Cargo",
        max_length=50,
        choices=ROLE_CHOICES
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Engineer(EnterpriseUser, AbstractUser):
    """
    Model representing an engineer, extending the base Django user and EnterpriseUser.

    Attributes:
        signature (str): The engineer’s signature (used in reports).
        groups (ManyToMany): Groups the engineer belongs to.
        user_permissions (ManyToMany): Permissions specific to the engineer.
    """

    signature = models.TextField("Firma", null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='engineer_set',
        blank=True,
        help_text='The groups this engineer belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='engineer_set',
        blank=True,
        help_text='Specific permissions for this engineer.',
        verbose_name='user permissions',
    )

    class Meta:
        verbose_name = "Ingeniero"
        verbose_name_plural = "Ingenieros"


class Client(EnterpriseUser):
    """
    Model representing a client user.

    Attributes:
        first_name (str): Client’s first name.
        last_name (str): Client’s last name.
    """

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
