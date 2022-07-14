from sqlalchemy import Column, ForeignKey, String, Enum, Integer, DateTime, func, UniqueConstraint
from sqlalchemy import func
from sqlalchemy.orm import relationship

from coins.models import choices
from coins.models.database import Base


class Coins(Base):
    __tablename__ = "coins"
    id = Column(Integer, primary_key=True)
    coin_id = Column(String, index=True, unique=True)
    coin_symbol = Column(String, index=True)
    coin_name = Column(String)
    contract_addresses = relationship("CoinsContract", back_populates="coin")
    created = Column(DateTime, server_default=func.now())
    
    
class CoinsContract(Base):
    __tablename__ = "coins_contract"
    
    id = Column(Integer, primary_key=True)
    platform = Column(String, index=True)
    contract_address = Column(String, index=True)
    coin_id = Column(Integer, ForeignKey("coins.id"))
    coin = relationship("Coins", back_populates="contract_addresses")
    created = Column(DateTime, server_default=func.now())
    
    UniqueConstraint(coin_id, contract_address, name="uc_coin_id_contract_address")
