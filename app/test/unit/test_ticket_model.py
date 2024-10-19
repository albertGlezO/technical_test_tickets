"""Test ticket model"""
#pylint: disable=E0401

import uuid
import unittest
import random
from app.models.ticket_model import TicketModels

class TestTicketModel(unittest.TestCase):
    """Test Event Model"""

    def setUp(self):
        self.input = {
            "event_id": random.randrange(1, 500),
            "ticket_hash": str(uuid.uuid4()),
            'redeem': 0,
        }

    def test_ticket_model(self):
        """ Function to verify the arguments in constructor
            - In the Ticket Model
            - Check the fields are defined correctly
            - When a new ticket is created
        """
        user = TicketModels(
            event_id = self.input.get('event_id'),
            ticket_hash = self.input.get('ticket_hash'),
            redeem = self.input.get('redeem'),
        )
        self.assertEqual(user.event_id, self.input.get('event_id'), 'Incorrect value')
        self.assertEqual(user.ticket_hash, self.input.get('ticket_hash'), 'Incorrect value')
        self.assertEqual(user.redeem, self.input.get('redeem'), 'Incorrect value')
