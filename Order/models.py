"""
Models for managing maintenance orders and protocols.

Includes:
- Order: Represents a work order for one or more devices.
- MaintenanceProtocol: Stores the maintenance report for a device in an order.
"""

from django.db import models


class Order(models.Model):
    """
    Represents a work order assigned to an engineer for one or more devices.

    Fields:
        engineer: The engineer responsible for the order.
        client: The institution or client receiving the service.
        contract: Optional contract linked to the order.
        client_AuthUser: The authenticated client user, if applicable.
        device: Devices included in the order.
        created_at: Timestamp of order creation.
        client_personal_name: Name of the client representative.
        client_sign: Signature of the client representative.
        status: Current status of the order (Scheduled, Completed, Delayed).
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
        blank=True,
    )
    client_AuthUser = models.ForeignKey(
        "AuthUser.Client",
        verbose_name="Cliente",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    device = models.ManyToManyField(
        "Device.Device",
        verbose_name="Equipos",
        related_name="included_devices",
        blank=True,
    )
    created_at = models.DateField(auto_now=True)
    client_personal_name = models.CharField(max_length=50, null=True, blank=True)
    client_sign = models.TextField(null=True, blank=True)
    status = models.CharField(
        "Estado de orden",
        max_length=50,
        choices=ORDER_STATUS,
    )

    class Meta:
        verbose_name = "Orden de trabajo"
        verbose_name_plural = "Ordenes de trabajo"

    def __str__(self):
        return f"Order {self.id} - Estado: {self.status}"


class MaintenanceProtocol(models.Model):
    """
    Stores the results of a maintenance protocol for a specific device within an order.

    Fields:
        device: The device being serviced.
        order: The order under which this protocol is executed.
        status: Final operational status of the device after maintenance.
        location: Physical location of the device during maintenance.
        fields: Flexible data for recording custom protocol fields (e.g., measurements, checklists).
    """

    MAINTENANCE_STATUS = [
        ("SR", "Sin revisar"),
        ("EPEN", "Equipo pendiente"),
        ("OPSO", "Equipo operativo sin observaciones"),
        ("OPCO", "Equipo operativo con observaciones"),
        ("SSTT", "Equipo se encuentra en servicio técnico"),
        ("ERBJ", "Equipo reportado de baja"),
        ("ENDB", "Equipo no disponible"),
    ]

    device = models.ForeignKey(
        "Device.Device",
        verbose_name="Equipo",
        on_delete=models.CASCADE,
        null=True,
    )
    order = models.ForeignKey(
        Order,
        verbose_name="Orden",
        on_delete=models.CASCADE,
        null=True,
    )
    status = models.CharField(
        "Estado final del equipo",
        max_length=50,
        choices=MAINTENANCE_STATUS,
        default="SR",
    )
    location = models.CharField("Ubicación", max_length=50, blank=True, null=True)
    fields = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        verbose_name = "Protocolo"
        verbose_name_plural = "Protocolos"

    def __str__(self):
        return (
            f"{self.device.device_model.part_number} - "
            f"{self.device.serial_number}: {self.status}"
        )
