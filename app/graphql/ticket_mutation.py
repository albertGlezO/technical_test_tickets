"""GraphQL mutations"""
#pylint: disable=E0401

import uuid
from datetime import datetime
import graphene

from graphql import GraphQLError
from app import db
from app.graphql.object import Ticket
from app.models.event_models import EventModels
from app.models.ticket_model import TicketModels

class BuyTicketMutation(graphene.Mutation):
    """Create ticket mutation class"""
    class Arguments:#pylint: disable=R0903
        """Arguments class"""
        event_id = graphene.Int(required=True)

    ticket = graphene.Field(lambda: Ticket)

    def mutate(self, info, event_id):#pylint: disable=W0613
        """Function to create the resource"""
        response, event = BussinessRulesTicket().bussiness_rules(
            event_id, return_event=True, apply=[1,5,6]
        )
        if response:
            raise GraphQLError(response)
        event.total_ticket_sales = event.total_ticket_sales + 1
        ticket = TicketModels(
            event_id=event_id,
            ticket_hash=str(uuid.uuid4()),
            redeem=0
        )
        db.session.add(ticket)
        db.session.commit()

        return BuyTicketMutation(ticket=ticket)

class RedeemTicketMutation(graphene.Mutation):
    """Create event mutation class"""
    class Arguments:#pylint: disable=R0903
        """Arguments class"""
        event_id = graphene.Int(required=True)
        ticket_id = graphene.Int(required=True)

    ticket = graphene.Field(lambda: Ticket)

    def mutate(self, info, event_id, ticket_id):#pylint: disable=R0913, W0613
        """Function to create the resource"""
        ticket = TicketModels().query.filter_by(id=ticket_id).first()
        response, event = BussinessRulesTicket().bussiness_rules(
            event_id, ticket, return_event=True, apply=[2, 3, 4, 6, 7]
        )
        if response:
            raise GraphQLError(response)
        event.total_ticket_redeem = event.total_ticket_redeem + 1
        ticket.redeem = 1
        db.session.commit()
        return RedeemTicketMutation(ticket=ticket)

class BussinessRulesTicket:#pylint: disable=R0903
    """Bussiness rules of ticket"""
    #pylint: disable=W0102, R0911
    def bussiness_rules(self, event_id, current_ticket = {}, return_event=False, apply=[1]):
        """Function to verify the conditional to manage an event"""
        event = EventModels().query.filter_by(id=event_id).first()
        event_from_datetime = None
        event_to_datetime = None
        if event:
            event_from_datetime = datetime.strptime(
                str(event.from_datetime), "%Y-%m-%d %H:%M:%S"
            )
            event_to_datetime = datetime.strptime(
                str(event.to_datetime), "%Y-%m-%d %H:%M:%S"
            )
        if 1 in apply and not event:
            return "Event not found", None
        if 2 in apply and not current_ticket:
            return "Ticket not found", None
        if 3 in apply and current_ticket and int(current_ticket.event_id) != int(event_id):
            return "Invalid operation, ticket is not from the event", None
        if 4 in apply and current_ticket and int(current_ticket.redeem) == 1:
            return "Invalid operation, ticket redeemed", None
        if 5 in apply and int(event.total_tickets) <= int(event.total_ticket_sales):
            return "Invalid operation, sold out", None
        if 6 in apply and event_to_datetime and event_to_datetime <= datetime.now():
            return "Invalid operation, event finish", None
        if 7 in apply and event_from_datetime and event_from_datetime > datetime.now():
            return "Invalid operation, event has not started", None
        return None, event if return_event else None
