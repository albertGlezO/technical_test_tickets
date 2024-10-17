"""Ticket controller"""

from flask import jsonify
from app.models.ticket_model import TicketModels

class TicketController:
    """Ticket controller class"""

    def __init__(self):
        self.ticket_model = TicketModels()

    def index(self, event_id):
        """Function to get all tickets by an event"""
        return jsonify({'success': True, 'data': {"route": "tickets"}})

    def create(self, event_id):
        """Function to buy a tickets of an event"""
        return jsonify({'success': True, 'data': {"route": "Ticket buy"}})

    def update(self, event_id, ticket_id):
        """Function to redeem a ticket of an event"""
        return jsonify({'success': True, 'data': {"route": "Ticket redeem"}})
