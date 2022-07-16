from typing import Any

from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session

from coins.core.config import get_settings, Settings
from coins.models.database import get_db
from coins.models.schemas import ResponseModel
from coins.tasks.api_call_tasks.tasks import fetch_coins_list_and_update_db
from coins.services import crud as crud_service

route = APIRouter()

@route.post('/update_coins_list', response_model=ResponseModel)
def get_coins_and_update_db(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
):
    
    res = fetch_coins_list_and_update_db.delay()
    
    return ResponseModel(message=f" [x] task with id {res.id} enqueued to fetch all the tokens")


@route.post('/set_watch_for_price', response_model=ResponseModel)
def set_watch_for_price(
    coin_id: str,
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
):
    
    res = crud_service.set_watch_for_price_for_coin_with_coid_id(coin_id=coin_id, db=db)
    
    if res:
        return ResponseModel(message=f" [x] The coin with id {coin_id} successfuly set to watch the price for.")
    else:
        return ResponseModel(message=f" [x] Failed to set watch for price for this token check logs.")


@route.get('/get_coin_ids', response_model=ResponseModel)
def get_coin_ids(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
):
    
    res = crud_service.get_coin_ids(db=db)
    
    if len(res) == 0:
        return ResponseModel(message=f" [x] There are no coins in the db run update_coins_list api to update the list")       
    
    if res:
        return ResponseModel(message=res)
    else:
        return ResponseModel(message=f" [x] Failed to fetch coin ids check logs.")
        
        
@route.get('/get_watching_for_price_coin_ids', response_model=ResponseModel)
def get_watching_for_price_coin_ids(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
):
    
    res = crud_service.get_watched_for_price_coin_ids(db=db)
    
    if len(res) == 0:
        return ResponseModel(message=f" [x] Currently there are no coins under watch for price")     
    
    if res:
        return ResponseModel(message=res)
    else:
        return ResponseModel(message=f" [x] Failed to fetch coin ids under watch for price check logs.")        