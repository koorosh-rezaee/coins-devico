# misc imports
from celery import Task, group
from celery.utils.log import get_task_logger
from celery.exceptions import Reject


logger = get_task_logger(__name__)

# app imports
from coins.celery_app import app
from coins.core.config import settings
from coins.core.abstract_task import RpcCallTask
from coins.models.choices import SupportedPlatforms
from coins.models.dbmodels import Coins, CoinsContract
from coins.services import api_calls
from coins.services import crud as crud_service
from coins.tasks.crud_tasks import tasks as crud_tasks
from coins.providers.client import TokensClient



@app.task(base=RpcCallTask, bind=True, queue='node-rpc-call-queue')
def fetch_and_update_token_decimals_from_node(self: RpcCallTask, platform: str, contract_address: str):

    token_client: TokensClient = TokensClient(platform=platform)
    
    if not token_client.platform_is_supported:
        logger.error(f" [x] The platform {platform} is not yet supported")
        return None
    
    decimals = token_client.get_token_contract_decimals(contract_address=contract_address)
    
    if decimals is None:
        logger.error(f" [x] Something happened during the task to get decimals of \
            the token contract with address {contract_address} for the platform {platform}.")
        return None
    
    # add the token to the database
    res = crud_tasks.update_coin_contract_decmals.delay(platform, contract_address, decimals)
    logger.info(f" [x] a task to update the token contract {contract_address}\
        with decimals {decimals} for the platform {platform} with task_id: {res.id} enqueued.")
    return None
    
    
@app.task(base=RpcCallTask, bind=True, queue='node-rpc-call-queue')
def fetch_and_update_token_decimals_from_node_for_platform(self: RpcCallTask, platform: str):
    
    coins_contract_db_rows: CoinsContract = self.db.query(CoinsContract).\
        filter(CoinsContract.platform == platform).filter(CoinsContract.decimals == None).all()

    token_client: TokensClient = TokensClient(platform=platform)
    
    if not token_client.platform_is_supported:
        logger.error(f" [x] The platform {platform} is not yet supported")
        return None
    
    task_ids = []
    
    coin_contract_db: CoinsContract
    for coin_contract_db in coins_contract_db_rows:
        res = fetch_and_update_token_decimals_from_node.delay(coin_contract_db.platform, coin_contract_db.contract_address)
        task_ids.append(res.id)

    return task_ids

    


    
  
