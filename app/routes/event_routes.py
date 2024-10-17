"""Event routes"""
#pylint: disable=E0401

from flask import Blueprint
from app.controllers.event_controller import EventController

main = Blueprint('event_blueprint', __name__)
controller = EventController()

@main.route('/')
def index():
    """Function to define the GET method"""
    return controller.index()

@main.route('/<event_id>')
def show(event_id):
    """Function to define the GET by id method"""
    return controller.show(event_id)

@main.route('/', methods=['POST'])
def create():
    """Function to define the POST method"""
    return controller.create()

@main.route('/<event_id>', methods=['PUT'])
def update(event_id):
    """Function to define the PUT method"""
    return controller.update(event_id)

@main.route('/<event_id>', methods=['DELETE'])
def destroy(event_id):
    """Function to define the DELETE method"""
    return controller.destroy(event_id)
