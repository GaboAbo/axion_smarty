from django.test import TestCase
from django.utils import timezone

from Entity.models import Entity, Contract
from Order.models import Order, MaintenanceProtocol
from datetime import timedelta

from django.db import models


# Create your tests here.
class FakeEngineer(models.Model):
    name = models.CharField(max_length=50)


class FakeClient(models.Model):
    name = models.CharField(max_length=50)


class FakeDeviceModel(models.Model):
    part_number = models.CharField(max_length=50)


class FakeDevice(models.Model):
    device_model = models.ForeignKey(FakeDeviceModel, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50)


# === ACTUAL TEST CASES ===
class OrderModelTest(TestCase):
    def setUp(self):
        self.entity = Entity.objects.create(name="Hospital A", address="Main Street 1")
        self.contract = Contract.objects.create(
            entity=self.entity,
            number=1001,
            contract_type="PV",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=365)
        )
        self.engineer = FakeEngineer.objects.create(name="Ing. Mario")
        self.client_user = FakeClient.objects.create(name="Client Org")
        self.device_model = FakeDeviceModel.objects.create(part_number="ABC123")
        self.device = FakeDevice.objects.create(
            device_model=self.device_model,
            serial_number="SN001"
        )

    def test_order_creation(self):
        order = Order.objects.create(
            engineer=self.engineer,
            client=self.entity,
            contract=self.contract,
            client_AuthUser=self.client_user,
            client_personal_name="Carlos Ruiz",
            client_sign="(signed)",
            status="PR"
        )
        order.device.add(self.device)

        self.assertIsNotNone(order.pk)
        self.assertEqual(order.status, "PR")
        self.assertEqual(order.client.name, "Hospital A")
        self.assertEqual(str(order), f"Order {order.id} - Estado: {order.status}")


class MaintenanceProtocolModelTest(TestCase):
    def setUp(self):
        self.entity = Entity.objects.create(name="Clinic B", address="Avenida Norte")
        self.contract = Contract.objects.create(
            entity=self.entity,
            number=2002,
            contract_type="GT",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=180)
        )
        self.engineer = FakeEngineer.objects.create(name="Ing. Sofia")
        self.client_user = FakeClient.objects.create(name="Client Health Co")
        self.device_model = FakeDeviceModel.objects.create(part_number="XYZ789")
        self.device = FakeDevice.objects.create(
            device_model=self.device_model,
            serial_number="SN999"
        )
        self.order = Order.objects.create(
            engineer=self.engineer,
            client=self.entity,
            contract=self.contract,
            client_AuthUser=self.client_user,
            status="CT"
        )
        self.order.device.add(self.device)

    def test_protocol_creation(self):
        protocol = MaintenanceProtocol.objects.create(
            device=self.device,
            order=self.order,
            status="OPSO",
            location="2nd Floor",
            fields={"pressure": "OK", "voltage": "Stable"}
        )

        self.assertIsNotNone(protocol.pk)
        self.assertEqual(protocol.status, "OPSO")
        self.assertEqual(protocol.location, "2nd Floor")
        self.assertIn("pressure", protocol.fields)
        self.assertEqual(str(protocol), f"{self.device.device_model.part_number} - {self.device.serial_number}: {protocol.status}")
