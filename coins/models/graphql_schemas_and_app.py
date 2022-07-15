import strawberry
import asyncio
from typing import AsyncGenerator
from random import random

from strawberry.fastapi import GraphQLRouter



@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)
    
@strawberry.type
class Subscription:
    @strawberry.subscription
    async def price(self) -> AsyncGenerator[float, None]:
        while True:
            yield random()
            await asyncio.sleep(2)    
    
schema = strawberry.Schema(query=Query, subscription=Subscription)    

graphql_app = GraphQLRouter(schema)    