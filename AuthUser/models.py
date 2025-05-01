from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
class EnterpriseUser(models.Model):
    # Child model for Enterprise users(Company that provide/receive services)
    # entity: User entity
    # role: User role
    # sign: Signature for report purposes
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

    entity = models.ForeignKey("Entity.Entity", verbose_name="Entidad", on_delete=models.CASCADE)
    role = models.CharField("Cargo", max_length=50, choices=ROLE_CHOICES)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Engineer(EnterpriseUser, AbstractUser):
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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
