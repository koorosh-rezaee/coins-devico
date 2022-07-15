# misc imports
from redis import Redis
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# app imports
from coins.celery_app import app
from coins.core.abstract_task import PeriodicTask
from coins.core.config import settings

from coins.services import crud as crud_service
from coins.tasks.api_call_tasks import tasks as api_call_tasks
from coins.tasks.crud_tasks import tasks as crud_tasks
from coins.services import api_calls as api_call_service
from coins.models import schemas



# start the beat and the worker together
# the beat will produce tasks and the worker will consume them
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    
    # Calls fetch_and_update_under_watch_tokens_prices to produce price updating tasks every (price_watcher_interval_seconds) seconds
    sender.add_periodic_task(settings.price_watcher_interval_seconds, fetch_and_update_under_watch_tokens_prices.s(), name='Update Tokens Prices')      


@app.task(base=PeriodicTask, bind=True, queue='high-priority-api-call-queue')
def fetch_and_update_under_watch_tokens_prices(self: PeriodicTask):

    coin_ids_list: list = crud_service.get_watch_for_price_coin_ids(db=self.db)
    
    if len(coin_ids_list) == 0:
        # nothing to do
        return
    # preparing the comma separated coin ids to use in simple price api
    ids: str = ",".join(coin_ids_list)
    
    # Fetching the prices data
    prices_data = api_call_service.get_simple_price(ids=ids, vs_currencies="usd,cad") # for simplicity i used 'usd,cad'
    
    # generating a prices list to facilitate the action of saving data into redis and for data validation
    prices_list = []
    for item in prices_data.items():
        coin = schemas.Coin(coin_id=item[0])
        for currency, price in item[1].items():
            coin.prices.append(schemas.CoinPrice(currency=currency, price=price))
            prices_list.append(coin)
            
    # save the data to redis
    queuing_res_list = []
    coin: schemas.Coin
    coin_price: schemas.CoinPrice
    for coin in prices_list:
        for coin_price in coin.prices:
            # (coin_id=coin.coin_id, currency=coin_price.currency, price=coin_price.price)
            res = crud_tasks.set_coin_price_in_redis.delay(coin.coin_id, coin_price.currency, coin_price.price)
            queuing_res_list.append(res)
            
    return
    
    

        
        
