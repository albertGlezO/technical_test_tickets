"""GraphQL mutations"""
#pylint: disable=E0401

import uuid
import graphene

from app import db
from app.graphql.object import Event, Ticket
from app.models.event_models import EventModels
from app.models.ticket_model import TicketModels

class CreateEventMutation(graphene.Mutation):
    """Create event mutation class"""
    class Arguments:#pylint: disable=R0903
        """Arguments class"""
        name = graphene.String(required=True)
        from_datetime = graphene.String(required=True)
        to_datetime = graphene.String(required=True)
        total_tickets = graphene.Int(required=True)

    event = graphene.Field(lambda: Event)

    def mutate(self, info, name, from_datetime, to_datetime, total_tickets):#pylint: disable=R0913, W0613
        """Function to create the resource"""
        event = EventModels(
            name=name,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            total_tickets=total_tickets
        )
        db.session.add(event)
        db.session.commit()
        return CreateEventMutation(event=event)

class CreateTicketMutation(graphene.Mutation):
    """Create ticket mutation class"""
    class Arguments:#pylint: disable=R0903
        """Arguments class"""
        event_id = graphene.Int(required=True)

    ticket = graphene.Field(lambda: Ticket)

    def mutate(self, info, event_id):#pylint: disable=W0613
        """Function to create the resource"""
        event = EventModels().query.filter_by(id=event_id).first()
        if event:
            event.total_ticket_sales = event.total_ticket_sales + 1
        ticket = TicketModels(
            event_id=event_id,
            ticket_hash=str(uuid.uuid4()),
            redeem=0
        )
        db.session.add(ticket)
        db.session.commit()

        return CreateTicketMutation(ticket=ticket)

class Mutation(graphene.ObjectType):#pylint: disable=R0903
    """Mutation class"""
    mutate_create_event = CreateEventMutation.Field()
    mutate_create_ticket = CreateTicketMutation.Field()
