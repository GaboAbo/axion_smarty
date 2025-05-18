"""
Test cases for the AuthUser app models.

Includes tests for the Engineer and Client models, ensuring proper creation,
relationships, and functionality of their fields.
"""

from django.test import TestCase
from django.contrib.auth.models import Group
from Entity.models import Entity
from .models import Engineer, Client


class EngineerModelTestCase(TestCase):
    """
    Test case for the Engineer model.

    This test case covers the creation and validation of an Engineer instance,
    including its relationships and attributes such as username, role, signature,
    and the entity it belongs to.
    """

    def setUp(self):
        """
        Set up the necessary data for the tests.

        Creates an entity and an engineer instance for use in the test cases.
        """
        self.entity = Entity.objects.create(name="Test Entity")
        self.engineer = Engineer.objects.create(
            username="test_engineer",
            entity=self.entity,
            role="ENG",
            signature="Test Signature"
        )

    def test_engineer_creation(self):
        """
        Test the creation of an engineer.

        Verifies that the engineer instance has been created correctly with the
        expected attributes.
        """
        self.assertEqual(self.engineer.username, "test_engineer")
        self.assertEqual(self.engineer.role, "ENG")
        self.assertEqual(self.engineer.signature, "Test Signature")
        self.assertEqual(self.engineer.entity, self.entity)

    def test_engineer_groups(self):
        """
        Test adding groups to an engineer.

        Verifies that the engineer can have multiple groups and that groups can
        be correctly added to the engineer's group set.
        """
        group = Group.objects.create(name="Test Group")
        self.engineer.groups.add(group)
        self.assertIn(group, self.engineer.groups.all())


class ClientModelTestCase(TestCase):
    """
    Test case for the Client model.

    This test case covers the creation and validation of a Client instance,
    ensuring that the client's fields, such as role and entity relationship,
    are correctly set.
    """

    def setUp(self):
        """
        Set up the necessary data for the tests.

        Creates an entity and a client instance for use in the test cases.
        """
        self.entity = Entity.objects.create(name="Test Entity")
        self.client = Client.objects.create(
            entity=self.entity,
            role="REP"
        )

    def test_client_creation(self):
        """
        Test the creation of a client.

        Verifies that the client instance has been created with the correct
        role and entity.
        """
        self.assertEqual(self.client.role, "REP")
        self.assertEqual(self.client.entity, self.entity)
