"""GraphQL query"""
#pylint: disable=E0401

import graphene
from graphene import relay

from app.graphql.object import Event
from app.models.event_models import EventModels


class Query(graphene.ObjectType):
    """Query class"""
    node = relay.Node.Field()

    events = graphene.List(lambda: Event, id=graphene.String())

    def resolve_events(self, info, id=None):#pylint: disable=W0622
        """Fucntion to get resources"""
        query = Event.get_query(info)
        if id:
            query = query.filter(EventModels.id == id)
        return query.all()
