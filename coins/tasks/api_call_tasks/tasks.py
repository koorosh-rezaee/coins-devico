# misc imports
from celery import Task, group
from celery.utils.log import get_task_logger
from celery.exceptions import Reject


logger = get_task_logger(__name__)

# app imports
from coins.celery_app import app
from coins.core.config import settings
from coins.core.abstract_task import APICallTask
from coins.models.dbmodels import Coins
from coins.services import api_calls
from coins.services import crud as crud_service
from coins.tasks.crud_tasks import tasks as crud_tasks



@app.task(base=APICallTask, bind=True, queue='api-call-queue')
def fetch_coins_list_and_update_db(self: APICallTask):

    coins_list: list = api_calls.get_coins_list(include_platform= False)
    
    if coins_list is None:
        raise Reject(reason="Failed to fetch coins list", requeue=False)
    
    # If successfull then we create coins in batches
    args_list = [list(item.values()) for item in coins_list]
    res = crud_tasks.create_new_coin_record.chunks(args_list, 10).apply_async()
    
    # if res.successful():
    #     logger.info(f" [x] Fetching coins lists and updating the db was successful")
    # else:
    #     logger.error(f" [x] Fetching coins lists and updating the db FAILED")
    
  
@app.task(base=APICallTask, bind=True, queue='api-call-queue')
def fetch_all_coins_contracts_and_update_db(self: APICallTask):
    """Fetching the coin data and adding its data to the db relating to its coins table
    """
    try:
        args_list = crud_service.read_id_and_coin_id_for_all_coins(db=self.db)
        
        if args_list is None:
            raise Reject(reason="Could not fetch coins id and coin_id from table Coins or there are None", requeue=False)
    
        results = []
        for args in args_list:
            res = fetch_coin_contracts_and_update_db.apply_async(args=args)
            results.append(res)
    
    except Exception as e:
        raise Reject(reason="Could not update token contracts because: {e}", requeue=False)
    # if res.successful():
    #     logger.info(f" [x] Fetching coin with id {coin_id} data and updating the db was successful")
    # else:
    #     logger.info(f" [x] Fetching coin with id {coin_id} data and updating the db FAILED")  
    
    
@app.task(base=APICallTask, bind=True, queue='api-call-queue')
def fetch_coin_contracts_and_update_db(self: APICallTask,  coin_db_id: int, coin_id: str):
    """Fetching the coin data and adding its data to the db relating to its coins table
    """
    
    coin_data: dict = api_calls.get_coin_data(id=coin_id)
    
    if coin_data is None:
        raise Reject(reason="Failed to fetch coin {coin_id}'s data", requeue=False)
    
    if 'platforms' not in coin_data.keys():
        raise Reject(reason="There are no platform key in the data of the coin with id {coin_id}", requeue=False)
    
    platforms: dict = coin_data['platforms']
    platform: dict
    
    args_list = [(platform_contract_pair[0], platform_contract_pair[1], coin_db_id, coin_id) for platform_contract_pair in platforms.items()]
    
    res = crud_tasks.create_new_coin_contract_record.chunks(args_list, 10).apply_async()
    
    # if res.successful():
    #     logger.info(f" [x] Fetching coin with id {coin_id} data and updating the db was successful")
    # else:
    #     logger.info(f" [x] Fetching coin with id {coin_id} data and updating the db FAILED")
    
    
@app.task(base=APICallTask, bind=True, queue='api-call-queue')
def fetch_coin_contracts(self: APICallTask,  coin_db_id: int, coin_id: str):
    """Fetching the coin data and adding its data to the db relating to its coins table
    """
    
    coin_data: dict = api_calls.get_coin_data(id=coin_id)
    
    if coin_data is None:
        raise Reject(reason="Failed to fetch coin {coin_id}'s data", requeue=False)
    
    if 'platforms' not in coin_data.keys():
        raise Reject(reason="There are no platform key in the data of the coin with id {coin_id}", requeue=False)
    
    platforms: dict = coin_data['platforms']
    platform: dict
    
    args_list = [(platform_contract_pair[0], platform_contract_pair[1], coin_db_id, coin_id) for platform_contract_pair in platforms.items()]
    
    return args_list
    
    
@app.task(base=APICallTask, bind=True, queue='high-priority-queue')
def say_hi(self: APICallTask):
    """Fetching the coin data and adding its data to the db relating to its coins table
    """
    print("------------HIIIIIIII--------------------------")
