from typing import Union, List, Dict, Any, Optional

from pydantic import BaseModel


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True

    error: bool = False
    number: int = 1
    message: Union[List, Dict, str]



class CoinPrice(BaseModel):
    class Config:
        orm_mode = True
    
    currency: str
    price: float


class Coin(BaseModel):
    class Config:
        orm_mode = True

    coin_id: str = None
    coin_symbol: Optional[str] = None
    coin_name: Optional[str] = None
    prices: Optional[List[CoinPrice]] = []
    