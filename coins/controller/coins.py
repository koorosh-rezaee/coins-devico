from typing import Any

from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session

from coins.core.config import get_settings, Settings
from coins.models.database import get_db
from coins.models.schemas import ResponseModel

route = APIRouter()

@route.get('/', response_model=ResponseModel)
def get_coins(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
):
    

    return ResponseModel(message="test")


@route.get('/update_coins_list', response_model=ResponseModel)
def get_coins(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
):
    

    return ResponseModel(message="test")

