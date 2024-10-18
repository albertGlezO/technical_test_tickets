"""Ticket controller"""
#pylint: disable=E0401

import uuid
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

    def create(self, event_id):
        """Function to buy a tickets of an event"""
        try:
            status_code, message, event = self.bussiness_rules(
                event_id, return_event=True
            )
            if status_code not in (200, 201, 202):
                return self.formatt_response(
                    status_code, message, event
                )
            new_ticket = TicketModels(event_id, str(uuid.uuid4()), 0)
            db.session.add(new_ticket)
            db.session.commit()
            response = self.formatt_response(
                200, "Create successful", {
                "id": new_ticket.id,
                "event_id": new_ticket.event_id,
                "event_name": event.name,
                "ticket_hash": new_ticket.ticket_hash,
                "redeem": new_ticket.redeem
            })
        except exc.SQLAlchemyError as err:
            response = self.formatt_response(
                500, "Internal server error", [err]
            )
        return response

    def update(self, event_id, ticket_id):
        """Function to redeem a ticket of an event"""
        try:
            status_code, message, event = self.bussiness_rules(
                event_id, return_event=True
            )
            if status_code not in (200, 201, 202):
                return self.formatt_response(
                    status_code, message, event
                )
            event.total_ticket_redeem = event.total_ticket_redeem + 1
            ticket = self.ticket_model.query.filter_by(id=ticket_id).first()
            ticket.redeem = 1
            db.session.commit()
            response = self.formatt_response(
                200, "Update successful", {
                "id": ticket.id,
                "event_id": ticket.event_id,
                "event_name": event.name,
                "ticket_hash": ticket.ticket_hash,
                "redeem": ticket.redeem
            })
        except exc.SQLAlchemyError as err:
            response = self.formatt_response(
                500, "Internal server error", [err]
            )
        return response

    #pylint: disable=W0102, R0911
    def bussiness_rules(self, event_id, current_ticket = {}, return_event=False):
        """Function to verify the conditional to manage an event"""
        event = self.event_model.query.filter_by(id=event_id).first()
        if not event:
            return self.formatt_response(
                400, "Event not found", {}
            )
        return 200, None, event if return_event else None
