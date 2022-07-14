# misc imports
from celery.utils.log import get_task_logger
from celery.exceptions import Reject


logger = get_task_logger(__name__)

# app imports
from coins.celery_app import app
from coins.core.config import settings
from coins.core.abstract_task import DBTask
from coins.models.dbmodels import Coins, CoinsContract



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
        
        


