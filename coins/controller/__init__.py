from fastapi import APIRouter, Depends

from coins.controller.coins import route as coins_route
from coins.models.graphql_schemas_and_app import graphql_app

route = APIRouter()
route.include_router(coins_route)
route.include_router(graphql_app, prefix="/graphql")

