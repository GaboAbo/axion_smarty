from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from .models import Entity, Contract, Area


class EntityModelTest(TestCase):
    """
    Test case for the Entity model.
    """

    def test_entity_creation(self):
        """
        Test that an Entity instance is created correctly and string representation matches its name.
        """
        entity = Entity.objects.create(
            name="Hospital San Juan",
            address="123 Calle Central"
        )
        self.assertIsNotNone(entity.pk)
        self.assertEqual(entity.name, "Hospital San Juan")
        self.assertEqual(str(entity), "Hospital San Juan")


class ContractModelTest(TestCase):
    """
    Test case for the Contract model.
    """

    def test_contract_creation(self):
        """
        Test that a Contract instance is created with valid data,
        is linked to an Entity, and its string representation is correct.
        """
        entity = Entity.objects.create(
            name="Hospital Central",
            address="Av. Principal 456"
        )
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=365)

        contract = Contract.objects.create(
            entity=entity,
            number=202501,
            contract_type="GT",
            start_date=start_date,
            end_date=end_date,
        )

        self.assertIsNotNone(contract.pk)
        self.assertEqual(contract.entity, entity)
        self.assertEqual(contract.contract_type, "GT")
        self.assertEqual(str(contract), f"{contract.number} - {contract.contract_type}")


class AreaModelTest(TestCase):
    """
    Test case for the Area model.
    """

    def test_area_creation(self):
        """
        Test that an Area instance is correctly created and linked to an Entity,
        and the string representation matches its name.
        """
        entity = Entity.objects.create(
            name="Clinica Norte",
            address="Calle 9, Zona 3"
        )
        area = Area.objects.create(
            entity=entity,
            name="Endoscopía"
        )

        self.assertIsNotNone(area.pk)
        self.assertEqual(area.entity, entity)
        self.assertEqual(area.name, "Endoscopía")
        self.assertEqual(str(area), "Endoscopía")
