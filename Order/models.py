from django.db import models

from Entity.models import Entity, Contract, Area


# Create your models here.
class Order(models.Model):
    """
    It stores an Order linked to a Client or Contract, as well as Devices
    device: Devices to perform maintenance
    """
    ORDER_STATUS = [
        ("PR", "Programada"),
        ("CT", "Completada"),
        ("AT", "Atradasa"),
    ]
    engineer = models.ForeignKey(
        "AuthUser.Engineer",
        verbose_name="Ingeniero",
        on_delete=models.CASCADE,
    )
    client = models.ForeignKey(
        "Entity.Entity",
        verbose_name="Entidad",
        on_delete=models.CASCADE,
    )
    contract = models.ForeignKey(
        "Entity.Contract",
        verbose_name="Contrato",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    client_AuthUser = models.ForeignKey(
        "AuthUser.Client",
        verbose_name="Cliente",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    device = models.ManyToManyField(
        "Device.Device",
        blank=True,
        verbose_name="Equipos",
        related_name='included_devices'
    )
    created_at = models.DateField(auto_now=True)
    client_personal_name = models.CharField(max_length=50, null=True, blank=True)
    client_sign = models.TextField(null=True, blank=True)
    status = models.CharField("Estado de orden", max_length=50, choices=ORDER_STATUS)

    class Meta:
        verbose_name = "Orden de trabajo"
        verbose_name_plural = "Ordenes de trabajo"

    def __str__(self):
        return f"Order {self.id} - Estado: {self.status}"


class MaintenanceProtocol(models.Model):
    """
    Base model for maintenance protocols
    device: Target Device
    order: Maintenance order
    status: Device's final status after maintenance
    fields: Custom fields, depending on the Device
    """
    MAINTENANCE_STATUS = [
        ("SR", "Sin revisar"),
        ("EPEN", "Equipo pendiente"),
        ("OPSO", "Equipo operativo sin observaciones"),
        ("OPCO", "Equipo operativo con observaciones"),
        ("SSTT", "Equipo se encuentra en servicio tecnico"),
        ("ERBJ", "Equipo reportado de baja"),
        ("ENDB", "Equipo no disponible")
    ]
    device = models.ForeignKey(
        "Device.Device",
        verbose_name="Equipo",
        on_delete=models.CASCADE,
        null=True
    )
    order = models.ForeignKey(
        Order,
        verbose_name="Orden",
        on_delete=models.CASCADE,
        null=True
    )
    status = models.CharField(
        "Estado final del equipo",
        max_length=50,
        choices=MAINTENANCE_STATUS,
        default='SR',
    )
    location = models.CharField("Ubicacion", max_length=50, blank=True, null=True)
    fields = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        verbose_name = "Protocolo"
        verbose_name_plural = "Protocolos"

    def __str__(self):
        return f"{self.device.device_model.part_number} - {self.device.serial_number}: {self.status}"
