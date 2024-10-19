"""Test event model"""
#pylint: disable=E0401

import unittest
import random
from faker import Faker
from app.models.event_models import EventModels

class TestEventModel(unittest.TestCase):
    """Test Event Model"""

    def setUp(self):
        fake = Faker()
        self.input = {
            "name": fake.name(),
            "from_datetime": (
                fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            ),
            'to_datetime': (
                fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            ),
            'total_tickets': random.randrange(1, 300),
            'total_ticket_sales': 0,
            'total_ticket_redeem': 0
        }

    def test_event_model(self):
        """ Function to verify the arguments in constructor
            - In the Event Model
            - Check the fields are defined correctly
            - When a new event is created
        """
        user = EventModels(
            name = self.input.get('name'),
            from_datetime = self.input.get('from_datetime'),
            to_datetime = self.input.get('to_datetime'),
            total_tickets = self.input.get('total_tickets'),
        )
        self.assertEqual(user.name, self.input.get('name'), 'Incorrect value')
        self.assertEqual(user.from_datetime, self.input.get('from_datetime'), 'Incorrect value')
        self.assertEqual(user.to_datetime, self.input.get('to_datetime'), 'Incorrect value')
        self.assertEqual(user.total_tickets, self.input.get('total_tickets'), 'Incorrect value')
        self.assertEqual(
            user.total_ticket_sales, self.input.get('total_ticket_sales'), 'Incorrect value'
        )
        self.assertEqual(
            user.total_ticket_redeem, self.input.get('total_ticket_redeem'), 'Incorrect value'
        )
