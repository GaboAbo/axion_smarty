from django.db import models


# Create your models here.
class Entity(models.Model):
    """
    Hospital/Clinic/Institute, stores its information
    name: Entity's name
    address: Entity's address
    """
    name = models.CharField("Nombre", max_length=255)
    address = models.CharField("Direccion", max_length=255)

    class Meta:
        verbose_name = "Entidad"
        verbose_name_plural = "Entidades"

    def __str__(self):
        return self.name


class Contract(models.Model):
    """
    Entity's contract information
    entity: Entity information
    number: Contract number
    contract_type: Contract type (Warranty/Post sales)
    start_date: Start date
    end_date: End date
    conditions*: File to check detailed information
    """
    CONTRACT_CHOICES = [
        ("GT", "Garantia"),
        ("PV", "Post Venta"),
    ]

    entity = models.ForeignKey(Entity, verbose_name="Entidad", on_delete=models.CASCADE)
    number = models.PositiveIntegerField("Numero")
    contract_type = models.CharField("Tipo", max_length=50, choices=CONTRACT_CHOICES, default="PV")
    start_date = models.DateField("Fecha de inicio", auto_now=False, auto_now_add=False)
    end_date = models.DateField("Fecha de fin", auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"

    def __str__(self):
        return f"{self.number} - {self.contract_type}"


class Area(models.Model):
    """
    Entity area
    entity: Entity
    name: Area name
    """
    entity = models.ForeignKey(Entity, verbose_name="Entidad", on_delete=models.CASCADE)
    name = models.CharField("Area", max_length=100)

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"
    
    def __str__(self):
        return self.name
