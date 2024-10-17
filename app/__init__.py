"""Application factory"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .database import mysql_db
from .routes import event_routes, ticket_routes

def create_app():
    """
        The application factory function
        - Create the Flask application and load configuration
        - Create de database object with SQLAlchemy constructor
        - Initialize the SQLAlchemy extencion
        - Load application components 'Blueprints'
    """

    app = Flask(__name__)
    app.config.from_object(mysql_db.get_connection())

    db = SQLAlchemy()
    db.init_app(app)
    with app.app_context():
        db.create_all()

    event_blueprints = event_routes.main
    ticket_blueprints = ticket_routes.main
    event_blueprints.register_blueprint(ticket_blueprints)
    app.register_blueprint(event_routes.main, url_prefix='/events')

    return app