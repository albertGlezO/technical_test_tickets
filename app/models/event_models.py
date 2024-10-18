"""Event models"""
#pylint: disable=W0611, E0401

import json
from flask import current_app
from app import db

#pylint: disable=R0913, R0903
class EventModels(db.Model):
    """Events models class"""
    __tablename__ = "events"

    def __init__(
            self,
            name=None,
            from_datetime=None,
            to_datetime=None,
            total_tickets=None,
            total_ticket_sales=0,
            total_ticket_redeem=0):
        self.name = name
        self.from_datetime = from_datetime
        self.to_datetime = to_datetime
        self.total_tickets = total_tickets
        self.total_ticket_sales = total_ticket_sales
        self.total_ticket_redeem = total_ticket_redeem

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    from_datetime = db.Column(db.DateTime)
    to_datetime = db.Column(db.DateTime)
    total_tickets = db.Column(db.Integer)
    total_ticket_sales = db.Column(db.Integer)
    total_ticket_redeem = db.Column(db.Integer)

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "from_datetime": str(self.from_datetime),
            "to_datetime": str(self.to_datetime),
            "total_tickets": self.total_tickets,
            "total_ticket_sales": self.total_ticket_sales,
            "total_ticket_redeem": self.total_ticket_redeem
        })