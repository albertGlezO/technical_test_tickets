from app import db

class EventModels(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    from_datetime = db.Column(db.DateTime)
    to_datetime = db.Column(db.DateTime)
    total_tickets = db.Column(db.Integer)
    total_ticket_sales = db.Column(db.Integer)
