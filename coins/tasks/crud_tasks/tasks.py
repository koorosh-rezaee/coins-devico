# misc imports
from celery.utils.log import get_task_logger
from celery.exceptions import Reject

from coins.services import crud


logger = get_task_logger(__name__)

# app imports
from coins.celery_app import app
from coins.core.config import settings
from coins.core.abstract_task import DBTask
from coins.models.dbmodels import Coins, CoinsContract



@app.task(base=DBTask, bind=True, queue='tokens-decimal-crud-queue')
def update_coin_contract_decmals(self: DBTask, platform: str, contract_address: str, decimals: int):
    
    # this should return just one record
    coin_contract: CoinsContract = self.db.query(CoinsContract).\
        filter(CoinsContract.platform == platform).\
            filter(CoinsContract.contract_address == contract_address).first()
            
    coin_contract.decimals = decimals
    try:
        self.db.add(coin_contract)
        self.db.commit()
        return
    except Exception as e:
        self.db.rollback()
        logger.info(f" [x] Could not update the decimals {decimals} for\
            the coin contract {contract_address} of the platform {platform} because: {e}")
        raise Reject(e, requeue=False)


@app.task(base=DBTask, bind=True, queue='crud-queue')
def create_new_coin_record(self: DBTask, coin_id: str, coin_symbol: str, coin_name:str):
    some_coin = Coins(
        coin_id=coin_id,
        coin_symbol=coin_symbol,
        coin_name=coin_name
    )
    try:
        self.db.add(some_coin)
        self.db.commit()
        return
    except Exception as e:
        self.db.rollback()
        logger.info(f" [x] Creating the coin with id {coin_id} failed because: {e}")
        raise Reject(e, requeue=False)
    
    
@app.task(base=DBTask, bind=True, queue='crud-queue')
def create_new_coin_contract_record(self: DBTask, platform: str, contract_address: str, coin_db_id: int, coin_id: str):
    
    some_coin_contract = CoinsContract(
        platform = platform,
        contract_address = contract_address,
        coin_id = coin_db_id
    )
    
    try:
        self.db.add(some_coin_contract)
        self.db.commit()
        
        return
    
    except Exception as e:
        self.db.rollback()
        logger.info(f" [x] Creating the coin contract record with contract\
            address {contract_address} for coin with id {coin_id} failed because: {e}")
        
        raise Reject(e, requeue=False)
    
@app.task(base=DBTask, bind=True, queue='crud-queue')
def read_coins_db_id_and_coinid(self: DBTask) -> list:
    
    try:
        id_coinid_list = self.db.query(Coins.id, Coins.coin_id).all()
        return id_coinid_list
    except Exception as e:
        logger.info(f" [x] Could not fetch coins id and coin_id data from db because: {e}") 
            
        raise Reject(e, requeue=False)    
        
        
@app.task(base=DBTask, bind=True, queue='crud-queue')
def set_coin_price_in_redis(self: DBTask, coin_id: str, currency: str, price: float) -> list:
    
    try:
        res = crud.set_prices_in_redis(coin_id=coin_id, currency=currency, price=price, r=self.r)
        return res
    except Exception as e:
        logger.error(f" [x] Could not set the price for coin {coin_id} and currency {currency} with the price {price} because: {e}") 
            
        raise Reject(e, requeue=False)   
