from web3 import Web3
from web3.middleware import geth_poa_middleware
from loguru import logger

from coins.providers.abi import BEP20_ABI
from coins.core.config import settings


class Bep20Token:
    w3: Web3 = None

    def __init__(self) -> None:
        w3 = Web3(Web3.HTTPProvider(settings.bsc_node_http_url))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)    
        self.w3 = w3


    def get_token_contract_decimals(self, contract_address: str) -> float:        
        try:
            token_contract = self.w3.eth.contract(
                address=contract_address,
                abi=BEP20_ABI
            )
            
            decimals = token_contract.functions.decimals().call()
            return decimals
        except Exception as e:
            logger.error(f" [x] Could not get token decimals on BSC provider with address {contract_address} because: {e}")