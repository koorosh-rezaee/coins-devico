from loguru import logger
from sqlalchemy.orm import Session

from coins.models.dbmodels import Coins



def read_id_and_coin_id_for_all_coins(db: Session):
    try:
        id_coinid_list = db.query(Coins.id, Coins.coin_id).all()
        # formatting the output from sqlalchemy to be json serializable
        id_coinid_list_formatted = [[row[0], row[1]] for row in id_coinid_list]
        return id_coinid_list_formatted
    except Exception as e:
        logger.info(f" [x] Could not fetch coins id and coin_id data from db because: {e}") 
        return None