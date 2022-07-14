import requests
import json
from loguru import logger    


from coins.core.config import settings
    
    
def get_ping():
    ping_relative_url = '/ping'
    ping_absolute_url_path = settings.coingecko_api_v3_base_url + ping_relative_url
    params = {}        
    
    res = requests.get(ping_absolute_url_path, params=params)
        
    return res
    
def get_coins_list(include_platform: bool=False):
    
    coins_relative_url = '/coins/list'
    coins_absolute_url_path = settings.coingecko_api_v3_base_url + coins_relative_url
    params = {
        'include_platform':include_platform,
        }
    
    try:
        res = requests.get(coins_absolute_url_path, params=params)
        
        if res.status_code == 200:
            coins_list: list = json.loads(res.content)
        
            return coins_list
        else:
            logger.info(f" [x] Could not get the coins list because: {json.loads(res.content)}")
            
            return None
        
    except Exception as e:
        logger.error(f" [x] Getting coins list failed because: {e}")
        
        return None
    
def get_coin_data(
                id: str, 
                localization: bool = True, 
                market_data: bool = True, 
                community_data: bool = True, 
                developer_data: bool = True, 
                sparkline: bool = False
    ):
    
    coins_relative_url = f"/coins/{id}"
    coins_absolute_url_path = settings.coingecko_api_v3_base_url + coins_relative_url
    params = {
        'localization':localization,
        'market_data':market_data,
        'community_data':community_data,
        'developer_data':developer_data,
        'sparkline':sparkline,
        }
    
    try:
        res = requests.get(coins_absolute_url_path, params=params)
        
        if res.status_code == 200:
            coins_data: list = json.loads(res.content)
        
            return coins_data
        else:
            logger.info(f" [x] Could not get the coin data with id {id} because: {json.loads(res.content)}")
            
            return None
        
    except Exception as e:
        logger.info(f" [x] Could not get the coin data with id {id} because: {e}")
        
        return None    
    
    