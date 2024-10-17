
from app import db

class TicketModels(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    ticket_hash = db.Column(db.String(32))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    redeem = db.Column(db.Integer)
