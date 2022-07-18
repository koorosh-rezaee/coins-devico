from redis import Redis
import strawberry
from fastapi import Depends
import asyncio
from typing import AsyncGenerator
from random import random
import json
from enum import Enum
import typing

from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from coins.services import crud as crud_service
from coins.core.config import get_redis
from coins.models.database import get_db, Session
from coins.models import dbmodels


# The context to make crud services work
async def get_context(
    r: Redis = Depends(get_redis),
    db: Session= Depends(get_db)
):
    return {
        "r": r,
        "db": db
    }


@strawberry.type
class CoinSubscription:
    coin_id: str
    price: float
    currency: str
    
@strawberry.type
class CoinsContract:    
    platform: str
    contract_address: str
    decimals: typing.Optional[int]
    coin_id: 'Coins'


@strawberry.type
class Coins:
    coin_id: str
    coin_symbol: str
    coin_name: str
    watch_for_price: bool
    contract_addresses: typing.Optional[typing.List[CoinsContract]]
    
@strawberry.enum
class CurrencyInpuType(Enum):
    usd = "usd"
    cad = "cad"
    
@strawberry.type
class Subscription:
    @strawberry.subscription()
    async def price(self, coin_id: str, currency: CurrencyInpuType, info: Info) -> AsyncGenerator[CoinSubscription ,None]:
        while True:
            price = crud_service.get_price_from_redis(coin_id=coin_id, currency=currency.value, r=info.context['r'])
            yield CoinSubscription(coin_id=coin_id, price=price, currency=currency.value)
            await asyncio.sleep(1)
            
            
@strawberry.type
class Query:
    
    @strawberry.field
    def get_coins(self, coin_ids: typing.List[str],info: Info) -> typing.List[Coins]:
        coins_list = []
        
        coins: dbmodels.Coins =  crud_service.get_coins(coin_ids=coin_ids ,db=info.context['db'])
        
        coin: dbmodels.Coins
        for coin in coins:
            coin_t = Coins(coin_id=coin.coin_id, 
                           coin_symbol=coin.coin_symbol, 
                           coin_name=coin.coin_name,
                           watch_for_price=coin.watch_for_price,
                           contract_addresses=[])
            coins_contracts: typing.List[CoinsContract] = []
            contract_row: dbmodels.CoinsContract
            for contract_row in coin.contract_addresses:
                coin_t.contract_addresses.append(
                    CoinsContract(platform=contract_row.platform,
                                  contract_address=contract_row.contract_address, 
                                  decimals=contract_row.decimals,
                                  coin_id=coin_t)
                    )
            coins_list.append(coin_t)
            
        return coins_list
                       
           
    
schema = strawberry.Schema(query=Query, subscription=Subscription)    

graphql_app = GraphQLRouter(schema, context_getter=get_context)    