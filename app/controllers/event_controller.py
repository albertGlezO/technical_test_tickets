"""Event controller"""

from flask import jsonify
from app.models.event_models import EventModels

class EventController:
    """Event controller class"""

    def __init__(self):
        self.event_model = EventModels()

    def index(self):
        """Function to get all events"""
        return jsonify({
            'success': True, 
            'data': self.event_model.query.all()
        })

    def show(self, event_id):
        """Function to get an event by id"""
        return jsonify({'success': True, 'data': {"route": "event"}})

    def create(self):
        """Function to create an event"""
        return jsonify({'success': True, 'data': {"route": "Event created"}})

    def update(self, event_id):
        """Function to update an event by id"""
        return jsonify({'success': True, 'data': {"route": "Event updated"}})

    def destroy(self, event_id):
        """Function to destroy an event by id"""
        return jsonify({'success': True, 'data': {"route": "Event deleted"}})
