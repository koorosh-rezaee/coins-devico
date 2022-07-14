from typing import Union, List, Dict

from pydantic import BaseModel


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True

    error: bool = False
    number: int = 1
    message: Union[List, Dict, str]



class Coin(BaseModel):
    class Config:
        orm_mode = True

    coin_id: str = None
    coin_symbol: str = None
    coin_name: str = None
    
    def __init(self, id: str, symbol: str, name: str):
        self.coin_id = id
        self.coin_symbol = symbol
        self.coin_name = name