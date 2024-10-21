"""GraphQL schema"""
#pylint: disable=E0401

import graphene

from app.graphql.mutation import Mutation
from app.graphql.query import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
