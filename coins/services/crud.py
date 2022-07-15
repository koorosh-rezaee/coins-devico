from loguru import logger
from sqlalchemy.orm import Session
from redis import Redis

from coins.models.dbmodels import Coins



def read_id_and_coin_id_for_all_coins(db: Session):
    try:
        id_coinid_list = db.query(Coins.id, Coins.coin_id).all()
        # formatting the output from sqlalchemy to be json serializable
        id_coinid_list_formatted = [[row[0], row[1]] for row in id_coinid_list]
        return id_coinid_list_formatted
    except Exception as e:
        logger.info(f" [x] Could not fetch coins id and coin_id data from db because: {e}") 
        return None
    
    
def set_prices_in_redis(coin_id: str, currency: str, price: float, r: Redis):
    
    try:
        res = r.set(f"PRICE::{coin_id}::{currency}", price)
    except Exception as e:
        logger.error(f" [x] Could not set the price for coin with id {coin_id} and currency {currency} with the price {price} because: {e}")
        
        
def get_price_from_redis(coin_id: str, currency: str, r: Redis):
    
    try:
        res = r.get(f"PRICE::{coin_id}::{currency}")
        if res is None:
            return 0
        else:
            return float(res)
    except Exception as e:
        logger.error(f" [x] Could not get the price for coin with id {coin_id} and currency {currency} because: {e}")    