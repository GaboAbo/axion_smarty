"""
Signal handlers for the 'App' Django application.

This module handles model signals related to many-to-many relationships in Orders.
Specifically, it listens for when devices are added to an Order and creates the corresponding
MaintenanceProtocol entries based on the device model's specifications.
"""

import importlib

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from Order.models import Order, MaintenanceProtocol


@receiver(m2m_changed, sender=Order.device.through)
def create_protocols_for_order(sender, instance, action, pk_set, **kwargs):
    """
    Signal handler that creates MaintenanceProtocol entries when devices are added to an Order.

    Triggered after devices are added to the many-to-many `device` field of an `Order`.

    Args:
        sender (Model): The intermediate model for the many-to-many relationship.
        instance (Order): The Order instance to which devices are being added.
        action (str): The type of change. We only respond to 'post_add'.
        pk_set (set): Primary keys of the devices that were added.
        **kwargs: Additional keyword arguments provided by the signal system.

    Behavior:
        - For each newly added device, dynamically imports the corresponding device model class.
        - Retrieves the device-specific `fields` definition.
        - Ensures a `MaintenanceProtocol` is created or fetched for the order/device combination.
    """
    if action == "post_add":
        devices = instance.device.filter(pk__in=pk_set)
        for device in devices:
            # Get the device model type, used as the Python module and class name
            module_name = device.device_model.device_type
            full_module_name = f"App.DeviceModels.{module_name}"

            # Dynamically import the module and retrieve the fields/class
            module = importlib.import_module(full_module_name)
            fields = getattr(module, module_name)

            # Create or fetch the MaintenanceProtocol instance
            MaintenanceProtocol.objects.get_or_create(
                order=instance,
                device=device,
                fields=fields,
            )
