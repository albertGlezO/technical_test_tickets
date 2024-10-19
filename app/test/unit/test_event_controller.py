"""Test event controller"""
#pylint: disable=E0401

import unittest
import random
from copy import copy
from datetime import datetime, timedelta
from faker import Faker
from app.controllers.event_controller import EventController
from app.models.event_models import EventModels

class TestEventController(unittest.TestCase):
    """Test Event Controller"""

    def setUp(self):
        self.controller = EventController()
        self.body_param = self.__load_body_params()

    def test_1_total_ticket_allowed(self):
        """ Function to verify the bussiness rules
            - Check the total tickets allowed
        """
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.body_param, apply=[1]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_2_total_ticket_allowed_fail(self):
        """ Function to verify the bussiness rules
            - Check the total ticket allowed with invalid value '500'
        """
        body_param = copy(self.body_param)
        body_param.update({"total_tickets": 500})
        status_code, message, data = (
            self.controller.bussiness_rules(
                body_param, apply=[1]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[1], message)
        self.assertDictEqual(
            {"min_tickets": self.controller.min_tickets,
            "max_tickets": self.controller.max_tickets},
            data,
        )

    def test_3_total_ticket_allowed_fail(self):
        """ Function to verify the bussiness rules
            - Check the total ticket allowed with invalid value '0'
        """
        body_param = copy(self.body_param)
        body_param.update({"total_tickets": 0})
        status_code, message, data = (
            self.controller.bussiness_rules(
                body_param, apply=[1]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[1], message)
        self.assertDictEqual(
            {"min_tickets": self.controller.min_tickets,
            "max_tickets": self.controller.max_tickets},
            data,
        )

    def test_4_start_date_event(self):
        """ Function to verify the bussiness rules
            - Check the start date event
        """
        body_param = copy(self.body_param)
        tomorrow = datetime.now()+timedelta(days=1)
        body_param.update({
            "from_datetime": tomorrow.strftime("%Y-%m-%d %H:%M:%S")
        })
        status_code, message, data = (
            self.controller.bussiness_rules(
                body_param, apply=[2]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_5_start_date_event_fail(self):
        """ Function to verify the bussiness rules
            - Check the total ticket allowed with invalid value '0'
        """
        body_param = copy(self.body_param)
        yesterday = datetime.now()-timedelta(days=1)
        body_param.update({
            "from_datetime": yesterday.strftime("%Y-%m-%d %H:%M:%S")
        })
        status_code, message, data = (
            self.controller.bussiness_rules(
                body_param, apply=[2]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[2], message)
        self.assertDictEqual(
            {"current_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "from_datetime": datetime.strptime(body_param["from_datetime"], "%Y-%m-%d %H:%M:%S")},
            data,
        )

    def test_6_start_date_range(self):
        """ Function to verify the bussiness rules
            - Check the range in dates
        """
        body_param = copy(self.body_param)
        yesterday = datetime.now()-timedelta(days=1)
        tomorrow = datetime.now()+timedelta(days=1)
        body_param.update({
            "from_datetime": yesterday.strftime("%Y-%m-%d %H:%M:%S"),
            "to_datetime": tomorrow.strftime("%Y-%m-%d %H:%M:%S")
        })
        status_code, message, data = (
            self.controller.bussiness_rules(
                body_param, apply=[3]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_7_start_date_range_fail(self):
        """ Function to verify the bussiness rules
            - Check the range in dates
        """
        body_param = copy(self.body_param)
        yesterday = datetime.now()-timedelta(days=1)
        tomorrow = datetime.now()+timedelta(days=1)
        body_param.update({
            "from_datetime": tomorrow.strftime("%Y-%m-%d %H:%M:%S"),
            "to_datetime": yesterday.strftime("%Y-%m-%d %H:%M:%S")
        })
        status_code, message, data = (
            self.controller.bussiness_rules(
                body_param, apply=[3]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[3], message)
        self.assertDictEqual(
            {"from_datetime": datetime.strptime(body_param["from_datetime"], "%Y-%m-%d %H:%M:%S"),
            "to_datetime": datetime.strptime(body_param["to_datetime"], "%Y-%m-%d %H:%M:%S")},
            data,
        )

    def test_8_start_date_range(self):
        """ Function to verify the bussiness rules
            - Check the length of time in event
        """
        body_param = copy(self.body_param)
        tomorrow = datetime.now()+timedelta(days=1)
        next_week = datetime.now()-timedelta(days=7)
        body_param.update({
            "from_datetime": tomorrow.strftime("%Y-%m-%d %H:%M:%S"),
            "to_datetime": next_week.strftime("%Y-%m-%d %H:%M:%S")
        })
        status_code, message, data = (
            self.controller.bussiness_rules(
                body_param, apply=[4]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_9_start_date_range_fail(self):
        """ Function to verify the bussiness rules
            - Check the length of time in event
        """
        body_param = copy(self.body_param)
        tomorrow = datetime.now()+timedelta(days=1)
        body_param.update({
            "from_datetime": tomorrow.strftime("%Y-%m-%d %H:%M:%S"),
            "to_datetime": tomorrow.strftime("%Y-%m-%d %H:%M:%S")
        })
        status_code, message, data = (
            self.controller.bussiness_rules(
                body_param, apply=[4]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[4], message)
        self.assertDictEqual(
            {"from_datetime": datetime.strptime(body_param["from_datetime"], "%Y-%m-%d %H:%M:%S"),
            "to_datetime": datetime.strptime(body_param["to_datetime"], "%Y-%m-%d %H:%M:%S")},
            data,
        )

    def test_10_total_ticket_sales(self):
        """ Function to verify the bussiness rules
            - Check if there are ticket sales
        """
        current_event = self.__load_current_event()
        current_event.total_tickets = current_event.total_tickets
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.body_param, current_event, apply=[5]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_11_total_ticket_sales_fail(self):
        """ Function to verify the bussiness rules
            - Check if there are ticket sales
        """
        body_param = copy(self.body_param)
        current_event = self.__load_current_event()
        body_param.update({
            "total_tickets": current_event.total_ticket_sales-10,
        })
        status_code, message, data = (
            self.controller.bussiness_rules(
                body_param, current_event, apply=[5]
            )
        )
        self.assertEqual(400, status_code, data)
        self.assertEqual(self.__load_fail_messages()[5], message)
        self.assertDictEqual(
            {"total_tickets": body_param["total_tickets"],
            "total_ticket_sales": int(current_event.total_ticket_sales)},
            data,
        )

    def test_12_unfinish_event(self):
        """ Function to verify the bussiness rules
            - Check unfinish event
        """
        yesterday = datetime.now()-timedelta(days=1)
        self.body_param.update({
            "from_datetime": yesterday.strftime("%Y-%m-%d %H:%M:%S"),
            "to_datetime": yesterday.strftime("%Y-%m-%d %H:%M:%S")
        })
        current_event = self.__load_current_event()
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.body_param, current_event, apply=[6]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_13_unfinish_event_fail(self):
        """ Function to verify the bussiness rules
            - Check unfinish event
        """
        yesterday = datetime.now()-timedelta(days=1)
        tomorrow = datetime.now()+timedelta(days=1)
        self.body_param.update({
            "from_datetime": yesterday.strftime("%Y-%m-%d %H:%M:%S"),
            "to_datetime": tomorrow.strftime("%Y-%m-%d %H:%M:%S")
        })
        current_event = self.__load_current_event()
        curremt_to_datetime = datetime.strptime(
            str(current_event.to_datetime), "%Y-%m-%d %H:%M:%S"
        )
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.body_param, current_event, apply=[6]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[6], message)
        self.assertDictEqual(
            {"current_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "to_datetime": curremt_to_datetime},
            data,
        )

    def test_14_unfinish_event(self):
        """ Function to verify the bussiness rules
            - Check if there are ticke sales
        """
        current_event = self.__load_current_event()
        current_event.total_ticket_sales = 0
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.body_param, current_event, apply=[7]
            )
        )
        self.assertEqual(200, status_code)
        self.assertEqual(None, message)
        self.assertEqual(None, data)

    def test_15_unfinish_event_fail(self):
        """ Function to verify the bussiness rules
            - Check if there are ticke sales
        """
        current_event = self.__load_current_event()
        current_event.total_ticket_sales = 10
        status_code, message, data = (
            self.controller.bussiness_rules(
                self.body_param, current_event, apply=[7]
            )
        )
        self.assertEqual(400, status_code)
        self.assertEqual(self.__load_fail_messages()[7], message)
        self.assertDictEqual(
            {"total_ticket_sales": int(current_event.total_ticket_sales)},
            data,
        )

    @staticmethod
    def __load_body_params():
        fake = Faker()
        return {
            "name": fake.name(),
            "from_datetime": (
                fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            ),
            'to_datetime': (
                fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            ),
            'total_tickets': random.randrange(1, 300)
        }

    def __load_current_event(self):
        return EventModels(
            name = self.body_param.get('name'),
            from_datetime = self.body_param.get('from_datetime'),
            to_datetime = self.body_param.get('to_datetime'),
            total_tickets = self.body_param.get('total_tickets'),
        )

    @staticmethod
    def __load_fail_messages():
        return {
            1 : "Invalid operation, allow 1 to 300 tickets",
            2 : "Invalid start date event",
            3 : "Invalid date range",
            4 : "Invalid length of time in event",
            5 : "Invalid operation, there are ticket sales",
            6 : "Invalid operation, unfinished event",
            7 : "Invalid operation, there are ticket sales"
        }
