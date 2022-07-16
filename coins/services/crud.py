from loguru import logger
from sqlalchemy.orm import Session
from redis import Redis

from coins.models.dbmodels import Coins



def get_coin_ids(db: Session):
    try:
        coin_in_dbs : Coins = db.query(Coins.coin_id).all()
        if coin_in_dbs is not None:
            
            formatted_coin_ids_list = [row[0] for row in coin_in_dbs]
            
            return formatted_coin_ids_list
        else:
            return None
    except Exception as e:
        logger.error(f" [x] Could not fetch coin ids: {e}")
        return False

def get_watched_for_price_coin_ids(db: Session):
    try:
        coin_in_dbs : Coins = db.query(Coins.coin_id).filter(Coins.watch_for_price == True).all()
        if coin_in_dbs is not None:
            
            formatted_coin_ids_list = [row[0] for row in coin_in_dbs]
            
            return formatted_coin_ids_list
        else:
            return None
    except Exception as e:
        logger.error(f" [x] Could not fetch coin ids: {e}")
        return False
    
def set_watch_for_price_for_coin_with_coid_id(coin_id: str, db: Session):
    try:
        coin_in_db: Coins = db.query(Coins).filter(Coins.coin_id == coin_id).first()
        if coin_in_db is not None:
            coin_in_db.watch_for_price = True
            db.add(coin_in_db)
            db.commit()
            
            return True
        else:
            return False
    except Exception as e:
        logger.error(f" [x] Could not set watch for price for token with id : {coin_id} because: {e}")
        return False
        
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
        
def get_watch_for_price_coin_ids(db: Session) -> list:

    try:
        coin_ids: Coins.coin_id = db.query(Coins.coin_id).filter(Coins.watch_for_price == True).all()
        return [row[0] for row in coin_ids]
    except Exception as e:
        logger.error(f" [x] Could not get coins to watch price because: {e}")
        return []
    
    
    