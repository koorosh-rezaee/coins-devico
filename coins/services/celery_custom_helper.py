from celery_app import app
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
        