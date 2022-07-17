from loguru import logger

from .interface import TokensInterface
from .ethereum import Erc20Token
from .bsc import Bep20Token
from .coingecko_supportet_platforms import PLATFORMS


class TokensClient:
    provider: TokensInterface = None
    platform: str = None

    def __init__(self, platform: str):
        
        self.platform = platform

        if platform not in PLATFORMS:
            self.provider = None
        elif platform == 'ethereum':
            self.provider = Erc20Token
        elif platform == 'binance-smart-chain':
            self.provider = Bep20Token
        # Todo: implement more providers to support more networks
        else:
            self.provider = None

    def get_token_contract_decimals(self, contract_address: str) -> int:
        if self.provider is not None:
            decimals = self.provider.get_token_contract_decimals(contract_address=contract_address)
            return decimals
        else:
            logger.info(f" [x] There is still no support for the platform {self.platform} in this service yet.")
            return None