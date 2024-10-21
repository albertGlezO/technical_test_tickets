"""GraphQL mutations"""
#pylint: disable=E0401

from datetime import datetime
import graphene


from graphql import GraphQLError
from app import db
from app.graphql.object import Event
from app.models.event_models import EventModels

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
        response = BussinessRulesEvent().bussiness_rules(
            {"name": name, "from_datetime": from_datetime,
             "to_datetime": to_datetime, "total_tickets": total_tickets},
            apply=[1,2,3,4]
        )
        if response:
            raise GraphQLError(response)
        db.session.add(event)
        db.session.commit()
        return CreateEventMutation(event=event)

class UpdateEventMutation(graphene.Mutation):
    """Create event mutation class"""
    class Arguments:#pylint: disable=R0903
        """Arguments class"""
        event_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        from_datetime = graphene.String(required=True)
        to_datetime = graphene.String(required=True)
        total_tickets = graphene.Int(required=True)

    event = graphene.Field(lambda: Event)

    def mutate(self, info, event_id, name, from_datetime, to_datetime, total_tickets):#pylint: disable=R0913, W0613
        """Function to create the resource"""
        event = EventModels().query.filter_by(id=event_id).first()
        response = BussinessRulesEvent().bussiness_rules(
            {"name": name, "from_datetime": from_datetime,
             "to_datetime": to_datetime, "total_tickets": total_tickets},
            event
        )
        if response:
            raise GraphQLError(response)
        event.name = name
        event.from_datetime = from_datetime
        event.to_datetime = to_datetime
        event.total_tickets = total_tickets
        db.session.commit()
        return UpdateEventMutation(event=event)

class DeleteEventMutation(graphene.Mutation):
    """Create event mutation class"""
    class Arguments:#pylint: disable=R0903
        """Arguments class"""
        event_id = graphene.Int(required=True)

    event = graphene.Field(lambda: Event)

    def mutate(self, info, event_id):#pylint: disable=R0913, W0613
        """Function to create the resource"""
        event = EventModels().query.filter_by(id=event_id).first()
        response = BussinessRulesEvent().bussiness_rules(
            {}, event, apply=[6,7]
        )
        if response:
            raise GraphQLError(response)
        db.session.delete(event)
        db.session.commit()
        return DeleteEventMutation(event=event)

class BussinessRulesEvent:
    """Bussiness rules of event"""
    #pylint: disable=W0102, R0911, R0903
    def __init__(self):
        self.min_tickets = 1
        self.max_tickets = 301

    def bussiness_rules(self, params, current_event = {}, apply=[1,2,3,4,5]):
        """
            Function to verify the conditional to manage an event
            - Verify total of tickets allowed
            - Verify invalid start date event
            - Verify invalid range dates
            - Verify length of time in event
            - Verify ticket sales to update the total ticket in event
            - Verify unfinished event to delete
            - Verify ticket sales to delete
        """
        from_datetime = None
        to_datetime = None
        curremt_to_datetime = None
        if params:
            from_datetime = datetime.strptime(
                params["from_datetime"], "%Y-%m-%d %H:%M:%S"
            )
            to_datetime = datetime.strptime(
                params["to_datetime"], "%Y-%m-%d %H:%M:%S"
            )
        if current_event:
            curremt_to_datetime = datetime.strptime(
                str(current_event.to_datetime), "%Y-%m-%d %H:%M:%S"
            )
        if 1 in apply and params["total_tickets"] not in range(self.min_tickets, self.max_tickets):
            return "Invalid operation, allow 1 to 300 tickets"
        if 2 in apply and from_datetime < datetime.now():
            return "Invalid start date event"
        if 3 in apply and from_datetime > to_datetime:
            return "Invalid date range"
        if 4 in apply and from_datetime == to_datetime:
            return "Invalid length of time in event"
        if 5 in apply and params["total_tickets"] < int(current_event.total_ticket_sales):
            return "Invalid operation, there are ticket sales"
        if 6 in apply and curremt_to_datetime and curremt_to_datetime > datetime.now():
            return "Invalid operation, unfinished event"
        if 7 in apply and current_event and int(current_event.total_ticket_sales) > 0:
            return "Invalid operation, there are ticket sales"
        return None
