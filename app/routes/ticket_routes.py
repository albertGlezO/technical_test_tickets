"""Ticket routes"""
#pylint: disable=E0401

from flask import Blueprint
from app.controllers.ticket_controller import TicketController

main = Blueprint('ticket_blueprint', __name__)
controller = TicketController()

@main.route('/<event_id>/tickets')
def index(event_id):
    """Function to define the GET method"""
    return controller.index(event_id)

@main.route('/<event_id>/tickets', methods=['POST'])
def buy(event_id):
    """Function to define the POST method"""
    return controller.buy(event_id)

@main.route('/<event_id>/tickets/<ticket_id>/redeem', methods=['PATCH'])
def redeem(event_id, ticket_id):
    """Function to define the PATCH method"""
    return controller.redeem(event_id, ticket_id)
