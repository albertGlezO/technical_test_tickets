"""Application factory"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from .database import mysql_db

db = SQLAlchemy()

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

    db.init_app(app)

    from app.schemas.schema import schema
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
        schema=schema,
        graphiql=True
        )
    )

    with app.app_context():
        from .routes import event_routes, ticket_routes
        event_blueprints = event_routes.main
        ticket_blueprints = ticket_routes.main
        event_blueprints.register_blueprint(ticket_blueprints)
        app.register_blueprint(event_routes.main, url_prefix='/events')

    return app
