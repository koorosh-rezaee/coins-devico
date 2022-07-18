from loguru import logger
from redis import Redis
from web3 import Web3

from coins.core.config import settings
from coins.providers.abi import ERC20_ABI
from .interface import TokensInterface


class Erc20Token(TokensInterface):
    w3: Web3 = None

    def __init__(self) -> None:
        self.w3 = Web3(Web3.HTTPProvider(settings.ethereum_node_http_url))
        
    def get_token_contract_decimals(self, contract_address: str) -> int:        
        try:
            checksum_address = self.w3.toChecksumAddress(contract_address)
            token_contract = self.w3.eth.contract(
                address=checksum_address,
                abi=ERC20_ABI
            )
            
            decimals = token_contract.functions.decimals().call()
            return decimals
        except Exception as e:
            logger.error(f" [x] Could not get token decimals on Ethereum provider with address {contract_address} because: {e}")
            return None