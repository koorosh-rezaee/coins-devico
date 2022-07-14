# misc imports
from celery.utils.log import get_task_logger
from celery.exceptions import Reject
from celery import chain

logger = get_task_logger(__name__)

# app imports
from coins.celery_app import app
from coins.core.config import settings
from coins.core.abstract_task import Workflow_Task
from coins.models.dbmodels import Coins, CoinsContract

from coins.tasks.api_call_tasks import tasks as api_call_tasks
from coins.tasks.crud_tasks import tasks as crud_tasks




    


