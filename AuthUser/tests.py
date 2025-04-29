from django.test import TestCase
from django.contrib.auth.models import Group
from Entity.models import Entity
from .models import Engineer, Client


# Create your tests here.
class EngineerModelTestCase(TestCase):
    def setUp(self):
        self.entity = Entity.objects.create(name="Test Entity")
        self.engineer = Engineer.objects.create(
            username="test_engineer",
            entity=self.entity,
            role="ENG",
            signature="Test Signature"
        )

    def test_engineer_creation(self):
        self.assertEqual(self.engineer.username, "test_engineer")
        self.assertEqual(self.engineer.role, "ENG")
        self.assertEqual(self.engineer.signature, "Test Signature")
        self.assertEqual(self.engineer.entity, self.entity)

    def test_engineer_groups(self):
        group = Group.objects.create(name="Test Group")
        self.engineer.groups.add(group)
        self.assertIn(group, self.engineer.groups.all())


class ClientModelTestCase(TestCase):
    def setUp(self):
        self.entity = Entity.objects.create(name="Test Entity")
        self.client = Client.objects.create(
            entity=self.entity,
            role="REP"
        )

    def test_client_creation(self):
        self.assertEqual(self.client.role, "REP")
        self.assertEqual(self.client.entity, self.entity)