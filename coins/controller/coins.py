from typing import Any

from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session
from redis import Redis

from coins.core.config import get_redis, get_settings, Settings
from coins.models.database import get_db
from coins.models.schemas import ResponseModel
from coins.tasks.api_call_tasks.tasks import fetch_coins_list_and_update_db, fetch_all_coins_contracts_and_update_db
from coins.services import crud as crud_service
from coins.services import celery_custom_helper as celery_helper_service

route = APIRouter()

@route.post('/update_coins_table', response_model=ResponseModel)
def update_coins_table(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
):
    
    res = fetch_coins_list_and_update_db.delay()
    
    return ResponseModel(message=f" [x] task with id {res.id} enqueued to fetch all the tokens")


@route.post('/update_coins_contracts_table', response_model=ResponseModel)
def update_coins_contracts_table(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    r: Redis = Depends(get_redis),
    forced: bool = False
):
    
    try:
        
        # if there is no coin ids in the db first run the fetch coins plan and prompt the user
        # to wait a second or two and then retry this plan
        
        coin_ids = crud_service.get_coin_ids(db=db)
        
        if (coin_ids is not None) and (coin_ids != False):
            if len(coin_ids) == 0:
                res = fetch_coins_list_and_update_db.delay()
                
                return ResponseModel(message=f" [x] There was no coin ids in db, task with id {res.id} enqueued to fetch all the coin ids please retry this plan after coin ids have been fetched.")
        
        if forced:
            revoked_properly = celery_helper_service.revoke_fetch_all_coins_contracts_and_update_db_tasks(r=r, force=True)
            if revoked_properly:
            
                res = fetch_all_coins_contracts_and_update_db.delay()
                
                # get the task ids to set in redis
                task_ids = res.get()
                
                if (task_ids is None) or (task_ids == False):
                    return ResponseModel(message=f" Encountered some errors check logs")
                    
                number_of_tasks_enqueud = crud_service.set_update_contracts_task_ids_in_redis(task_ids=task_ids, r=r)
                
                if not number_of_tasks_enqueud:
                    return ResponseModel(message=f" Encountered some errors check logs")
                
                progress = celery_helper_service.get_progress_fetch_all_coins_contracts_and_update_db(r=r)
                return ResponseModel(message=f" [x] Forced revoked the fetching contracts plan and a number of {number_of_tasks_enqueud} tasks enqueued to fetch all the tokens contracts with progress: {progress}")   
            
            else:
                ResponseModel(message=" [x] Could not properly revoke the running plan please check logs")  
        
        else:               
        
            # check if there are running tasks
            task_ids = crud_service.get_update_contracts_task_ids_in_redis(r=r)
            
            # if there are no in progress tasks to fetch contract addresses then run the plan
            if task_ids is None:
                res = fetch_all_coins_contracts_and_update_db.delay()
                
                # get the task ids to set in redis
                task_ids = res.get()
                
                number_of_tasks_enqueud = crud_service.set_update_contracts_task_ids_in_redis(task_ids=task_ids, r=r)
                
                # if could not keep the track of tasks then just call off the plan and revoke them all
                if not number_of_tasks_enqueud:
                    revoked = celery_helper_service.revoke_task_ids(task_ids=task_ids, force=True)
                    
                    if revoked:
                        logger.error(f" [x] could not save the {len(task_ids)} task ids in redis so revoked them all.")
                        return ResponseModel(message=f" Encountered some errors check logs")        
                    else:
                        logger.error(f" [x] could not revoke {len(task_ids)} task ids either!.")
                        return ResponseModel(message=f" Encountered some errors check logs")        
                else:
                    progress = celery_helper_service.get_progress_fetch_all_coins_contracts_and_update_db(r=r)
                    return ResponseModel(message=f" [x] A number of {number_of_tasks_enqueud} tasks enqueued to fetch all the tokens contracts with progress: {progress}")

            # if there is an error
            elif task_ids == False:
                return ResponseModel(message=f" Encountered some errors check logs")
            
            # there is still an in progress plan
            else:
                progress = celery_helper_service.get_progress_fetch_all_coins_contracts_and_update_db(r=r)
                return ResponseModel(message=f" [x] There is still an in progress plan if its stucked you can force to rerun the plan, progress: {progress}")
        
    except Exception as e:
        logger.error(f" [x] something happened during the calling  /update_coins_contracts_table and it was: {e}")
        return ResponseModel(message=f" Encountered some errors check logs")


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