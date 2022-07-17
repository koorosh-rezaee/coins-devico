from loguru import logger
from redis import Redis
from web3 import Web3

from coins.core.config import settings
from coins.providers.abi import ERC20_ABI


class Erc20Token:
    w3: Web3 = None

    def __init__(self, w3: Web3) -> None:
        self.w3 = Web3(Web3.HTTPProvider(settings.eth_url))
        
    def get_token_contract_decimals(self, contract_address: str) -> float:        
        try:
            token_contract = self.w3.eth.contract(
                address=contract_address,
                abi=ERC20_ABI
            )
            
            decimals = token_contract.functions.decimals().call()
            return decimals
        except Exception as e:
            logger.error(f" [x] Could not get token decimals on Ethereum provider with address {contract_address} because: {e}")