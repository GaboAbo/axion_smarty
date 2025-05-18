"""
Unit tests for the Order and MaintenanceProtocol models.
"""

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from AuthUser.models import Engineer, Client
from Entity.models import Entity, Contract
from Device.models import Device, DeviceModel
from Order.models import Order, MaintenanceProtocol


class OrderModelTest(TestCase):
    """
    Test case for Order and MaintenanceProtocol model behaviors.
    """

    def setUp(self):
        """
        Create related models for testing:
        - Entity (client)
        - Engineer
        - Client AuthUser
        - Contract
        - DeviceModel
        - Device
        - Order (with M2M device)
        - MaintenanceProtocol
        """

        # Entity (acts as the client organization)
        self.client = Entity.objects.create(
            name="Test Clinic",
            address="123 Main Street"
        )

        # Engineer user
        self.engineer = Engineer.objects.create_user(
            username="testengineer",
            password="securepass123",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            entity=self.client,
            role="ENG",
            is_active=True,
            is_staff=False
        )

        # Individual Client (AuthUser role)
        self.client_AuthUser = Client.objects.create(
            first_name="Foo",
            last_name="Fighter",
            entity=self.client,
            role="TEN"
        )

        # Contract between the Entity and system
        self.contract = Contract.objects.create(
            entity=self.client,
            number=1001,
            contract_type="PV",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=365)
        )

        # Device model reference
        self.device_model = DeviceModel.objects.create(
            device_type="END",
            device_gen="EX3",
            part_number="GIF-H190"
        )

        # Physical device instance
        self.device = Device.objects.create(
            client=self.client,
            contract=self.contract,
            device_model=self.device_model,
            serial_number="SN123456"
        )

        # Create an order for maintenance
        self.order = Order.objects.create(
            engineer=self.engineer,
            client=self.client,
            contract=self.contract,
            client_AuthUser=self.client_AuthUser,
            status="PR"
        )

        # Associate the device with the order (M2M)
        self.order.device.set([self.device])

        # MaintenanceProtocol attached to the order/device
        self.protocol = MaintenanceProtocol.objects.create(
            order=self.order,
            device=self.device,
            status="SR",
            fields={"Electronics": "Replaced power board"}
        )

    def test_order_str_representation(self):
        """
        Test the __str__ method of the Order model.
        """
        expected = f"Order {self.order.pk} - Estado: PR"
        self.assertEqual(str(self.order), expected)

    def test_protocol_str_representation(self):
        """
        Test the __str__ method of the MaintenanceProtocol model.
        """
        expected = f"{self.device.device_model.part_number} - {self.device.serial_number}: SR"
        self.assertEqual(str(self.protocol), expected)
