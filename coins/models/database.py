from loguru import logger
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import registry
from sqlalchemy.orm import scoped_session


from coins.core.config import settings

db_args = {"check_same_thread": False} if settings.postgresql_url.startswith('sqlite') else {}

engine = create_engine(settings.postgresql_url, connect_args=db_args, pool_recycle=settings.db_connection_recycle_seconds, pool_size=settings.db_pool_size)

# to be used for fast api and scope the session in a request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped db session in order to be used in celery tasks to overcome concurrency using threading.local() 
ScopedSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine)) 

Base: registry = declarative_base()
logger.info("Init Database from address: %s" % settings.postgresql_url)


# when called using fastapi dependencies it returns a db session scoped to that request only and 
# retrieves the session before the request ends
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
