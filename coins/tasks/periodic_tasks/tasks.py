# misc imports
import queue
import time
from celery import Task
from sqlalchemy.orm import Session
from redis import Redis
from celery.utils.log import get_task_logger
from celery.schedules import crontab

logger = get_task_logger(__name__)

# app imports
from coins.celery_app import app
from coins.core.abstract_task import PeriodicTask
from coins.core.custom_exceptions import SomethingBadHappened
from coins.core.config import settings


# start the beat and the worker together
# the beat will produce tasks and the worker will consume them
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    
    # Calls produce_bnb_watcher_tasks every watcher_period_seconds seconds
    sender.add_periodic_task(settings.price_watcher_interval_seconds, fetch_and_update_under_watch_tokens_prices.s(), name='Update Tokens Prices')      


@app.task(base=PeriodicTask, bind=True, queue='high-priority-api-call-queue')
def fetch_and_update_under_watch_tokens_prices(self):
    pass

        
        
