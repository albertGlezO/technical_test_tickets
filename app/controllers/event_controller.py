"""Event controller"""
#pylint: disable=E0401

from flask import request
from sqlalchemy import exc
from app.controllers.base_controller import BaseController
from app import db
from app.models.event_models import EventModels

class EventController(BaseController):
    """Event controller class"""

    def __init__(self):
        self.event_model = EventModels()

    def index(self):
        """Function to get all events"""
        try:
            result = []
            data = self.event_model.query.all()
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

    def show(self, event_id):
        """Function to get an event by id"""
        try:
            data = self.event_model.query.filter_by(id=event_id).first()
            result = self.convert_object_to_dict(data)
            response = self.formatt_response(
                200, "Success", result
            )
        except exc.SQLAlchemyError:
            response = self.formatt_response(
                500, "Internal server error", []
            )
        return response

    def create(self):
        """Function to create an event"""
        try:
            b_params = request.json
            new_event = EventModels(
                b_params["name"],
                b_params["from_datetime"],
                b_params["to_datetime"],
                b_params["total_tickets"]
            )
            db.session.add(new_event)
            db.session.commit()
            response = self.formatt_response(
                200, "Create successful", {
                "id": new_event.id,
                "name": new_event.name,
                "from_datetime": new_event.from_datetime,
                "to_datetime": new_event.to_datetime,
                "total_tickets": new_event.total_tickets,
                "total_ticket_sales": new_event.total_ticket_sales,
                "total_ticket_redeem": new_event.total_ticket_redeem
            })
        except KeyError as err:
            response = self.formatt_response(
                500, "Body param required", [str(err)]
            )
        except exc.SQLAlchemyError:
            response = self.formatt_response(
                500, "Internal server error", []
            )
        return response

    def update(self, event_id):
        """Function to update an event by id"""
        try:
            b_params = request.json
            event = self.event_model.query.filter_by(id=event_id).first()
            event.name = b_params.get("name")
            event.from_datetime = b_params.get("from_datetime")
            event.to_datetime = b_params.get("to_datetime")
            event.total_tickets = b_params.get("total_tickets")
            db.session.commit()
            response = self.formatt_response(
                200, "Update successful", {
                "id": event_id,
                "name": event.name,
                "from_datetime": event.from_datetime,
                "to_datetime": event.to_datetime,
                "total_tickets": event.total_tickets,
                "total_ticket_sales": event.total_ticket_sales,
                "total_ticket_redeem": event.total_ticket_redeem
            })
        except exc.SQLAlchemyError:
            response = self.formatt_response(
                500, "Internal server error", []
            )
        return response

    def destroy(self, event_id):
        """Function to destroy an event by id"""
        try:
            event = self.event_model.query.filter_by(id=event_id).first()
            db.session.delete(event)
            db.session.commit()
            response = self.formatt_response(
                200, "Destroy successful", {
                "affected_rows": 1,
            })
        except exc.SQLAlchemyError:
            response = self.formatt_response(
                500, "Internal server error", []
            )
        return response
