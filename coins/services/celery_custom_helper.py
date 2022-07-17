from coins.celery_app import app
from loguru import logger



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
                