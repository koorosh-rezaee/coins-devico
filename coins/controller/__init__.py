from fastapi import APIRouter, Depends

from coins.controller.coins import route as coins_route

route = APIRouter()
route.include_router(coins_route)
