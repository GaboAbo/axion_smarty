import importlib

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from Order.models import Order, MaintenanceProtocol


@receiver(m2m_changed, sender=Order.device.through)
def create_protocols_for_order(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        devices = instance.device.filter(pk__in=pk_set)
        for device in devices:
            module_name = device.device_model.device_type

            full_module_name = f"App.DeviceModels.{module_name}"

            module = importlib.import_module(full_module_name)
            fields = getattr(module, module_name)

            MaintenanceProtocol.objects.get_or_create(
                order=instance,
                device=device,
                fields=fields,
            )
