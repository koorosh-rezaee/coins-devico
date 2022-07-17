from loguru import logger
from redis import Redis

from coins.celery_app import app
from coins.services import crud as crud_service

def revoke_task_ids(task_ids: list, force: bool=False):
    try:
        if not force:
            for task_id in task_ids:
                app.control.revoke(task_id, terminate=True, signal='SIGTERM')
        else:
            for task_id in task_ids:
                app.control.revoke(task_id, terminate=True, signal='SIGKILL')
        return True
    except Exception as e:
        logger.error(f" [x] Could not revoke {len(task_ids)} task(s) because: {e}")


def get_task_ids_progress(task_ids: list) -> dict:
    
    total = len(task_ids)
    progress = {
        'total': total,
        'ready': 0,
        'successful': 0,
        'failed': 0
    }
    
    try:
        for task_id in task_ids:
            
            if app.AsyncResult(task_id).ready():
                progress['ready'] += 1
                
                if app.AsyncResult(task_id).successful():
                    progress['successful'] += 1
                elif app.AsyncResult(task_id).failed():
                    progress['failed'] += 1
                    
        return progress
    
    except Exception as e:
        logger.error(f" [x] Could not get the progress for {len(task_ids)} tasks because: {e}")
        return None
                
                

def get_progress_fetch_all_coins_contracts_and_update_db(r: Redis):
    
    try:
        # see if there is a redis key for TASK::fetch_all_coins_contracts_and_update_db
        task_ids = crud_service.get_update_contracts_task_ids_in_redis(r=r)
        
        if task_ids is None:
            return None
        
        progress: dict = get_task_ids_progress(task_ids=task_ids)
        
        return progress
    except Exception as e:
        logger.error(f" [x] Could not get the progress for fetch_all_coins_contracts_and_update_db tasks because: {e}")
        return None
    
def revoke_fetch_all_coins_contracts_and_update_db_tasks(r: Redis, force: bool):
    try:
        # see if there is a redis key for TASK::fetch_all_coins_contracts_and_update_db
        task_ids = crud_service.get_update_contracts_task_ids_in_redis(r=r)
        
        if task_ids is None:
            return None
        
        revoked_task_ids: bool = revoke_task_ids(task_ids=task_ids, force=force)
        
        if revoked_task_ids:
            deleted_key:bool = crud_service.delete_update_contracts_task_ids_in_redis(r=r)
            
            if not deleted_key:
                logger.error(f" [x] Could not delete the redis key TASKS::fetch_all_coins_contracts_and_update_db after revoking tasks")
        
        return revoked_task_ids and deleted_key
    except Exception as e:
        logger.error(f" [x] Could not revoke {len(task_ids)} task(s) because: {e}")
        return None    