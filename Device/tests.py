from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from Entity.models import Entity, Contract
from .models import DeviceModel, Device

# Create your tests here.
class DeviceModelTestCase(TestCase):
    def test_deviceModel_creation(self):
        deviceModel = DeviceModel.objects.create(
            device_type = "END",
            device_gen = "EX3",
            part_number = "GIF-HQ190",
        )

        self.assertEqual(str(deviceModel), f"{deviceModel.part_number}")


class DeviceTestCase(TestCase):
    def test_deviceModel_creation(self):
        client = Entity.objects.create(
            name="Hospital Central",
            address="Av. Principal 456"
        )
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=365)
        contract = Contract.objects.create(
            entity=client,
            number=202501,
            contract_type="GT",
            start_date=start_date,
            end_date=end_date,
        )
        device_model = DeviceModel.objects.create(
            device_type = "END",
            device_gen = "EX3",
            part_number = "GIF-HQ190",
        )
        serial_number = "2222333"

        device = Device.objects.create(
            client=client,
            contract=contract,
            device_model=device_model,
            serial_number=serial_number
        )

        self.assertIsNotNone(client.pk)
        self.assertIsNotNone(contract.pk)
        self.assertIsNotNone(device_model.pk)
        self.assertEqual(device.device_model, device_model)
        self.assertEqual(str(device), f"{device_model.part_number} - {serial_number}")