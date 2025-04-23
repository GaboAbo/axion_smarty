from django.db import models

from Entity.models import Entity, Contract, Area


# Create your models here.
class DeviceModel(models.Model):
    """
    It stores the Device Models generic information
    device_type: Category
    part_number: Device's part number
    """
    TYPE_CHOICES = [
        ("END", "Endoscopio flexible"),
        ("VPR", "Procesador de video"),
        ("LIS", "Fuente de luz"),
        ("PMP", "Bomba de irrigación"),
        ("INF", "Insuflador de CO²"),
        ("MON", "Monitor de grado médico"),
        ("WST", "Estación de trabajo"),
        ("TEL", "Telescopio"),
        ("ECG", "Unidad de electrocirugía"),
        ("UDI", "Sistema de documentación"),
    ]
    GENERATION_CHOICES = [
        ("OPT", "Optera (170)"),
        ("EX3", "Exera III (190)"),
        ("EX2", "Exera II (180)"),
        ("EX1", "Exera I (160)"),
        ("LUC", "Evis Lucera (270)"),
        ("LUE", "Evis Lucera Elite (290)"),
        ("EV3", "Evis Exera III (190)"),
        ("EV2", "Evis Exera II (180)"),
        ("VSR", "Visera (150/160)"),
        ("VSP", "Visera Pro"),
        ("VSE", "Visera Elite"),
        ("VS2", "Visera Elite II"),
        ("X1P", "X1 Series"),
        ("OIP", "Procesador de imágenes"),
        ("CV1", "Serie CV-100"),
        ("CV2", "Serie CV-200"),
        ("CV3", "Serie CV-300"),
        ("CV4", "Serie CV-400"),
        ("OES", "Serie OES"),
        ("PRO", "Serie PRO"),
        ("ULT", "Serie ULTRA"),
        ("FIB", "Fibroscopio de fibra óptica"),
        ("NOG", "Sin generacion")
    ]
    device_type = models.CharField("Tipo", max_length=100, choices=TYPE_CHOICES)
    device_gen = models.CharField("Generacion", max_length=100, choices=GENERATION_CHOICES)
    part_number = models.CharField("Modelo", max_length=100)

    class Meta:
        verbose_name = "Modelo"
        verbose_name_plural = "Modelos"

    def __str__(self):
        return self.part_number


class Device(models.Model):
    """
    It stores the Device specific information
    client: User to visit
    contract: Client's Contract, if exist
    device_model: Device's generic information
    serial_number: Comercial unique identifier
    """
    client = models.ForeignKey(
        "Entity.Entity",
        verbose_name="Entidad",
        on_delete=models.CASCADE,
        null=True
    )
    contract = models.ForeignKey(
        "Entity.Contract",
        verbose_name="Contrato",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    device_model = models.ForeignKey(
        DeviceModel,
        verbose_name="Equipo",
        related_name='model',
        on_delete=models.CASCADE,
        null=True
    )
    serial_number = models.CharField("Serie", max_length=100, unique=True)

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    def __str__(self):
        return f"{self.device_model.part_number} - {self.serial_number}"
    