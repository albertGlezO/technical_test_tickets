"""Ticket Models"""
#pylint: disable=W0611, E0401

import json
from flask import current_app
from app import db

#pylint: disable=R0903
class TicketModels(db.Model):
    """Ticket Models Class"""
    __tablename__ = "tickets"

    def __init__(self, event_id=None, ticket_hash=None, redeem=0):
        self.event_id = event_id
        self.ticket_hash = ticket_hash
        self.redeem = redeem

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    ticket_hash = db.Column(db.String(32))
    redeem = db.Column(db.Integer)

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "event_id": self.event_id,
            "ticket_hash": self.ticket_hash,
            "redeem": self.redeem
        })
