from redis import Redis
import strawberry
from fastapi import Depends
import asyncio
from typing import AsyncGenerator
from random import random
import json

from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from coins.services import crud as crud_service
from coins.core.config import get_redis


async def get_context(
    r: Redis = Depends(get_redis),
):
    return {
        "r": r,
    }


@strawberry.type
class User:
    name: str
    age: int    
    
@strawberry.type
class Subscription:
    @strawberry.subscription()
    async def price(self, coin_id: str, currency: str, info: Info) -> AsyncGenerator[float ,None]:
        while True:
            price = crud_service.get_price_from_redis(coin_id=coin_id, currency=currency, r=info.context['r'])
            yield price
            await asyncio.sleep(2)
            
            
@strawberry.type
class Query:
    
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)
    
    @strawberry.field
    def price(self, coin_id: str, currency: str) -> User:
        return Subscription(coin_id=coin_id, currency=currency)             
            
           
    
schema = strawberry.Schema(query=Query, subscription=Subscription)    

graphql_app = GraphQLRouter(schema, context_getter=get_context)    