"""GraphQL object"""
#pylint: disable=E0401

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models.event_models import EventModels
from app.models.ticket_model import TicketModels


class Event(SQLAlchemyObjectType):
    """Event class"""
    class Meta:#pylint: disable=R0903
        """Meta class"""
        model = EventModels
        interfaces = (relay.Node,)

    tickets = graphene.List(lambda: Ticket, ticket_hash=graphene.String(), redeem=graphene.Int())
    def resolve_tickets(self, info, ticket_hash=None, redeem=None):
        """Function to return the tickets event"""
        query = Ticket.get_query(info=info)
        query = query.filter(TicketModels.event_id == self.id)#pylint: disable=E1101
        if ticket_hash:
            query = query.filter(TicketModels.ticket_hash == ticket_hash)
        if redeem:
            query = query.filter(TicketModels.redeem == redeem)

        return query.all()

class Ticket(SQLAlchemyObjectType):
    """Ticket class"""
    class Meta:#pylint: disable=R0903
        """Meta class"""
        model = TicketModels
        interfaces = (relay.Node,)
