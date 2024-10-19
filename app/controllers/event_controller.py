"""Event controller"""
#pylint: disable=E0401

from datetime import datetime
from flask import request
from sqlalchemy import exc
from app.controllers.base_controller import BaseController
from app import db
from app.models.event_models import EventModels

class EventController(BaseController):
    """Event controller class"""

    def __init__(self):
        self.event_model = EventModels()
        self.min_tickets = 1
        self.max_tickets = 300

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
            status_code, message, data = self.bussiness_rules(
                b_params, apply=[1,2,3,4]
            )
            if status_code not in (200, 201, 202):
                return self.formatt_response(
                    status_code, message, data
                )
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
                500, "Internal server error", [err]
            )
        return response

    def update(self, event_id):
        """Function to update an event by id"""
        try:
            b_params = request.json
            event = self.event_model.query.filter_by(id=event_id).first()
            status_code, message, data = self.bussiness_rules(
                b_params, event
            )
            if status_code not in (200, 201, 202):
                return self.formatt_response(
                    status_code, message, data
                )
            event.name = b_params["name"]
            event.from_datetime = b_params["from_datetime"]
            event.to_datetime = b_params["to_datetime"]
            event.total_tickets = b_params["total_tickets"]
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
        except KeyError as err:
            response = self.formatt_response(
                500, "Body param required", [str(err)]
            )
        except exc.SQLAlchemyError:
            response = self.formatt_response(
                500, "Internal server error", []
            )
        return response

    def destroy(self, event_id):
        """Function to destroy an event by id"""
        try:
            event = self.event_model.query.filter_by(id=event_id).first()
            status_code, message, data = self.bussiness_rules({}, event, [6,7])
            if status_code not in (200, 201, 202):
                return self.formatt_response(
                    status_code, message, data
                )
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

    #pylint: disable=W0102, R0911
    def bussiness_rules(self, params, current_event = {}, apply=[1,2,3,4,5]):
        """
            Function to verify the conditional to manage an event
            - Verify total of tickets allowed
            - Verify invalid start date event
            - Verify invalid range dates
            - Verify length of time in event
            - Verify ticket sales to update the total ticket in event
            - Verify unfinished event to delete
            - Verify ticket sales to delete
        """
        from_datetime = None
        to_datetime = None
        curremt_to_datetime = None
        if params:
            from_datetime = datetime.strptime(
                params["from_datetime"], "%Y-%m-%d %H:%M:%S"
            )
            to_datetime = datetime.strptime(
                params["to_datetime"], "%Y-%m-%d %H:%M:%S"
            )
        if current_event:
            curremt_to_datetime = datetime.strptime(
                str(current_event.to_datetime), "%Y-%m-%d %H:%M:%S"
            )
        if 1 in apply and params["total_tickets"] not in range(self.min_tickets, self.max_tickets):
            return 400, "Invalid operation, allow 1 to 300 tickets", {
                "min_tickets": self.min_tickets,
                "max_tickets": self.max_tickets
            }
        if 2 in apply and from_datetime < datetime.now():
            return 400, "Invalid start date event", {
                "current_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "from_datetime": from_datetime
            }
        if 3 in apply and from_datetime > to_datetime:
            return 400, "Invalid date range", {
                "from_datetime": from_datetime,
                "to_datetime": to_datetime
            }
        if 4 in apply and from_datetime == to_datetime:
            return 400, "Invalid length of time in event", {
                "from_datetime": from_datetime,
                "to_datetime": to_datetime
            }
        if 5 in apply and params["total_tickets"] < int(current_event.total_ticket_sales):
            return 400, "Invalid operation, there are ticket sales", {
                "total_tickets": params["total_tickets"],
                "total_ticket_sales": int(current_event.total_ticket_sales)
            }
        if 6 in apply and curremt_to_datetime and curremt_to_datetime > datetime.now():
            return 400, "Invalid operation, unfinished event", {
                "current_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "to_datetime": curremt_to_datetime,
            }
        if 7 in apply and int(current_event.total_ticket_sales) > 0:
            return 400, "Invalid operation, there are ticket sales", {
                "total_ticket_sales": int(current_event.total_ticket_sales)
            }
        return 200, None, None
