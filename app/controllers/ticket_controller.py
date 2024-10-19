"""Ticket controller"""
#pylint: disable=E0401

import uuid
from datetime import datetime
from sqlalchemy import exc
from app.controllers.base_controller import BaseController
from app import db
from app.models.event_models import EventModels
from app.models.ticket_model import TicketModels

class TicketController(BaseController):
    """Ticket controller class"""

    def __init__(self):
        self.ticket_model = TicketModels()
        self.event_model = EventModels()
        self.event_id = None

    def index(self, event_id):
        """Function to get all tickets by an event"""
        try:
            result = []
            status_code, message, event = self.bussiness_rules(
                event_id
            )
            if status_code not in (200, 201, 202):
                return self.formatt_response(
                    status_code, message, event
                )
            data = self.ticket_model.query.filter_by(event_id=event_id).all()
            for item in data:
                data_converted = self.convert_object_to_dict(item)
                result.append(data_converted)
            response = self.formatt_response(
                200, "Success", result
            )
        except exc.SQLAlchemyError:
            response = self.formatt_response(
                500, "Internal server error", []
            )
        return response

    def buy(self, event_id):
        """Function to buy a tickets of an event"""
        try:
            status_code, message, event = self.bussiness_rules(
                event_id, return_event=True, apply=[1,5,6]
            )
            if status_code not in (200, 201, 202):
                return self.formatt_response(
                    status_code, message, event
                )
            event.total_ticket_sales = event.total_ticket_sales + 1#pylint:disable=E1101
            new_ticket = TicketModels(event_id, str(uuid.uuid4()), 0)
            db.session.add(new_ticket)
            db.session.commit()
            response = self.formatt_response(
                200, "Create successful", {
                "id": new_ticket.id,
                "event_id": new_ticket.event_id,
                "event_name": event.name,#pylint:disable=E1101
                "ticket_hash": new_ticket.ticket_hash,
                "redeem": new_ticket.redeem
            })
        except exc.SQLAlchemyError as err:
            response = self.formatt_response(
                500, "Internal server error", [err]
            )
        return response

    def redeem(self, event_id, ticket_id):
        """Function to redeem a ticket of an event"""
        try:
            ticket = self.ticket_model.query.filter_by(id=ticket_id).first()
            status_code, message, event = self.bussiness_rules(
                event_id, ticket, return_event=True, apply=[2, 3, 4,6]
            )
            if status_code not in (200, 201, 202):
                return self.formatt_response(
                    status_code, message, event
                )
            event.total_ticket_redeem = event.total_ticket_redeem + 1#pylint:disable=E1101
            ticket.redeem = 1
            db.session.commit()
            response = self.formatt_response(
                200, "Update successful", {
                "id": ticket.id,
                "event_id": ticket.event_id,
                "event_name": event.name,#pylint:disable=E1101
                "ticket_hash": ticket.ticket_hash,
                "redeem": ticket.redeem
            })
        except exc.SQLAlchemyError as err:
            response = self.formatt_response(
                500, "Internal server error", [err]
            )
        return response

    #pylint: disable=W0102, R0911
    def bussiness_rules(self, event_id, current_ticket = {}, return_event=False, apply=[1]):
        """Function to verify the conditional to manage an event"""
        self.event_id = event_id
        event = self.get_event()
        event_to_datetime = None
        if event:
            event_to_datetime = datetime.strptime(
                str(event.to_datetime), "%Y-%m-%d %H:%M:%S"
            )
        if 1 in apply and not event:
            return 400, "Event not found", {}
        if 2 in apply and not current_ticket:
            return 400, "Ticket not found", {}
        if 3 in apply and current_ticket and int(current_ticket.event_id) != int(event_id):
            return 400, "Invalid operation, ticket is not from the event", {}
        if 4 in apply and current_ticket and int(current_ticket.redeem) == 1:
            return 400, "Invalid operation", {"redeem": 1}
        if 5 in apply and int(event.total_tickets) <= int(event.total_ticket_sales):
            return 400, "Invalid operation, sold out", {
                "total_tickets": event.total_tickets,
                "total_ticket_sales": event.total_ticket_sales
            }
        if 6 in apply and event_to_datetime and event_to_datetime <= datetime.now():
            return 400, "Invalid operation, event finish", {
                "current_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "to_datetime": event_to_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            }
        return 200, None, event if return_event else None

    def get_event(self):
        """Function to get the event object by id given"""
        return self.event_model.query.filter_by(id=self.event_id).first()
