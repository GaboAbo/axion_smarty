from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from Entity.models import Entity, Contract
from Device.models import DeviceModel, Device


class DeviceModelTestCase(TestCase):
    def test_device_model_creation(self):
        """
        Test creation of a DeviceModel instance and its string representation.
        """
        model = DeviceModel.objects.create(
            device_type="END",
            device_gen="EX3",
            part_number="GIF-HQ190",
        )

        self.assertEqual(str(model), "GIF-HQ190")
        self.assertEqual(model.device_type, "END")
        self.assertEqual(model.device_gen, "EX3")


class DeviceTestCase(TestCase):
    def setUp(self):
        """
        Create common Entity, Contract, and DeviceModel for device creation test.
        """
        self.client = Entity.objects.create(
            name="Hospital Central",
            address="Av. Principal 456"
        )
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=365)

        self.contract = Contract.objects.create(
            entity=self.client,
            number=202501,
            contract_type="GT",
            start_date=start_date,
            end_date=end_date,
        )

        self.device_model = DeviceModel.objects.create(
            device_type="END",
            device_gen="EX3",
            part_number="GIF-HQ190",
        )

    def test_device_creation(self):
        """
        Test creation of a Device and its relationships and string output.
        """
        serial_number = "2222333"
        device = Device.objects.create(
            client=self.client,
            contract=self.contract,
            device_model=self.device_model,
            serial_number=serial_number
        )

        self.assertEqual(device.device_model, self.device_model)
        self.assertEqual(device.client, self.client)
        self.assertEqual(device.contract, self.contract)
        self.assertEqual(device.serial_number, serial_number)
        self.assertEqual(str(device), "GIF-HQ190 - 2222333")
