"""Test ticket controller"""
#pylint: disable=E0401

import uuid
import random
from datetime import datetime, timedelta
from copy import copy
from unittest import TestCase
from unittest.mock import MagicMock
from faker import Faker
from app.controllers.ticket_controller import TicketController
from app.models.event_models import EventModels
from app.models.ticket_model import TicketModels

class TestTicketController(TestCase):
    """Test Ticket Controller"""

    def setUp(self):
        self.controller = TicketController()
        self.event_id = random.randrange(1, 500)
        self.current_event = self.__load_current_event()
        self.current_ticket = self.__load_current_ticket()

    def test_1_event_not_found(self):
        """ Function to verify the bussiness rules
            - Check if the event exist
        """

        self.controller.get_event = MagicMock(return_value=self.current_event)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, apply=[1]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_2_event_not_found_fail(self):
        """ Function to verify the bussiness rules
            - Check if the event exist
        """

        self.controller.get_event = MagicMock(return_value=None)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, apply=[1]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[1], message)
        self.assertDictEqual({},data)

    def test_3_ticket_not_found(self):
        """ Function to verify the bussiness rules
            - Check if the ticket exist
        """

        self.controller.get_event = MagicMock(return_value=self.current_event)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, current_ticket=self.current_ticket, apply=[2]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_4_ticket_not_found_fail(self):
        """ Function to verify the bussiness rules
            - Check if the event exist
        """

        self.controller.get_event = MagicMock(return_value=None)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, apply=[2]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[2], message)
        self.assertDictEqual({},data)

    def test_5_ticket_is_not_of_event(self):
        """ Function to verify the bussiness rules
            - Check if the ticket is of the event given
        """
        current_event = copy(self.current_event)
        current_event.id = self.event_id
        self.controller.get_event = MagicMock(return_value=current_event)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, current_ticket=self.current_ticket, apply=[3]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_6_ticket_is_not_of_event_fail(self):
        """ Function to verify the bussiness rules
            - Check if the ticket is of the event given
        """
        current_event = copy(self.current_event)
        current_event.id = self.event_id
        self.controller.get_event = MagicMock(return_value=current_event)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id+1, current_ticket=self.current_ticket, apply=[3]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[3], message)
        self.assertDictEqual({},data)

    def test_7_redeem(self):
        """ Function to verify the bussiness rules
            - Check if the ticket is redeem
        """
        self.controller.get_event = MagicMock(return_value=self.current_event)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, current_ticket=self.current_ticket, apply=[4]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_8_redeem_fail(self):
        """ Function to verify the bussiness rules
            - Check if the ticket is redeem
        """
        current_ticket = copy(self.current_ticket)
        current_ticket.redeem = 1
        self.controller.get_event = MagicMock(return_value=self.current_event)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, current_ticket=current_ticket, apply=[4]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[4], message)
        self.assertDictEqual({'redeem': current_ticket.redeem}, data)

    def test_9_sold_out(self):
        """ Function to verify the bussiness rules
            - Check the sold out
        """
        self.controller.get_event = MagicMock(return_value=self.current_event)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, apply=[5]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_10_sold_out_fail(self):
        """ Function to verify the bussiness rules
            - Check the sold out
        """
        current_event = copy(self.current_event)
        current_event.total_ticket_sales = current_event.total_tickets
        self.controller.get_event = MagicMock(return_value=current_event)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, apply=[5]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[5], message)
        self.assertDictEqual(
            {'total_ticket_sales': current_event.total_ticket_sales,
             'total_tickets': current_event.total_tickets},
            data
        )

    def test_11_event_finished(self):
        """ Function to verify the bussiness rules
            - Check if the event finished
        """
        tomorrow = datetime.now()+timedelta(days=1)
        next_week = datetime.now()+timedelta(days=7)
        current_event = copy(self.current_event)
        current_event.from_datetime = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
        current_event.to_datetime = next_week.strftime("%Y-%m-%d %H:%M:%S")
        self.controller.get_event = MagicMock(return_value=current_event)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, apply=[6]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_12_event_finished_fail(self):
        """ Function to verify the bussiness rules
            - Check if the event finished
        """
        last_week = datetime.now()-timedelta(days=1)
        yesterday = datetime.now()-timedelta(days=1)
        current_event = copy(self.current_event)
        current_event.from_datetime = last_week.strftime("%Y-%m-%d %H:%M:%S")
        current_event.to_datetime = yesterday.strftime("%Y-%m-%d %H:%M:%S")
        self.controller.get_event = MagicMock(return_value=current_event)
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.event_id, apply=[6]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[6], message)
        self.assertDictEqual(
            {"current_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "to_datetime": current_event.to_datetime},
            data
        )

    def __load_current_event(self):
        fake = Faker()
        return EventModels(
            name = fake.name(),
            from_datetime = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            to_datetime = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            total_tickets = random.randrange(1, 300),
        )

    def __load_current_ticket(self):
        return TicketModels(
            event_id = self.event_id,
            ticket_hash = str(uuid.uuid4()),
            redeem = 0
        )

    @staticmethod
    def __load_fail_messages():
        return {
            1 : "Event not found",
            2 : "Ticket not found",
            3 : "Invalid operation, ticket is not from the event",
            4 : "Invalid operation",
            5 : "Invalid operation, sold out",
            6 : "Invalid operation, event finish"
        }
