from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from AuthUser.models import Engineer, Client
from Entity.models import Entity, Contract
from Device.models import Device, DeviceModel
from Order.models import Order, MaintenanceProtocol

# Create your tests here.
class OrderModelTest(TestCase):
    def setUp(self):
        # Create Entity
        self.entity = Entity.objects.create(
            name="Test Clinic",
            address="123 Main Street"
        )

        # Create Engineer
        self.engineer = Engineer.objects.create_user(
            username="testengineer",
            password="securepass123",
            first_name="John",
            last_name="Doe",
            entity=self.entity,
            role="ENG"
        )

        # Create Client
        self.client = Entity.objects.create(
            first_name="Client",
            last_name="User",
            entity=self.entity,
            role="DOC"
        )

        # Create Contract
        self.contract = Contract.objects.create(
            entity=self.entity,
            number=1001,
            contract_type="PV",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=365)
        )

        # Create DeviceModel
        self.device_model = DeviceModel.objects.create(
            device_type="END",
            device_gen="EX3",
            part_number="GIF-H190"
        )

        # Create Device
        self.device = Device.objects.create(
            client=self.entity,
            contract=self.contract,
            device_model=self.device_model,
            serial_number="SN123456"
        )

        # Create Order
        self.order = Order.objects.create(
            engineer=self.engineer,
            entity=self.entity,
            contract=self.contract,
            client=self.client,
            maintenance_type="COR",
            failure_type="ELC",
            entry_date=timezone.now(),
            state="NEW"
        )

        # Associate Device with Order (M2M)
        self.order.device.set([self.device])

        # Create MaintenanceProtocol
        self.protocol = MaintenanceProtocol.objects.create(
            order=self.order,
            device=self.device,
            service_type="COR",
            observations="Replaced power board"
        )

    def test_order_str_representation(self):
        self.assertEqual(str(self.order), f"OT-{self.order.pk}")

    def test_protocol_str_representation(self):
        expected_str = f"{self.device.device_model.part_number} - {self.device.serial_number}"
        self.assertEqual(str(self.protocol), expected_str)
