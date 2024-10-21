"""GraphQL mutations"""
#pylint: disable=E0401

import graphene

from app.graphql.event_mutation import CreateEventMutation, UpdateEventMutation, DeleteEventMutation
from app.graphql.ticket_mutation import BuyTicketMutation, RedeemTicketMutation

class Mutation(graphene.ObjectType):#pylint: disable=R0903
    """Mutation class"""
    mutate_create_event = CreateEventMutation.Field()
    mutate_update_event = UpdateEventMutation.Field()
    mutate_delete_event = DeleteEventMutation.Field()
    mutate_buy_ticket = BuyTicketMutation.Field()
    mutate_redeem_ticket = RedeemTicketMutation.Field()
