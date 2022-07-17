# misc imports
from celery import Task
from requests import Session
from sqlalchemy.orm.scoping import scoped_session
from redis import Redis

# app imports
from coins.core.custom_exceptions import SomethingBadHappened
from coins.models.database import ScopedSession
from coins.core.config import settings


class DBTask(Task):
        
    _db: scoped_session = None
    _redis: Redis = None

    @property
    def r(self) -> Redis:
        if self._redis is None:
            self._redis = Redis(host=settings.redis_url.host, port=settings.redis_url.port, db=int(settings.redis_url.path.strip('/')), decode_responses=True)
        return self._redis           

    @property
    def db(self) -> scoped_session:
        if self._db is None:
            self._db = ScopedSession()
        return self._db    

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        
       pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))    
        
        
class PeriodicTask(Task):
            
    _db: scoped_session = None
    _redis: Redis
    
    abstract = True
    # retries the task on the Exceptions it can be customized to raise Exceptions based on unwanted results
    autoretry_for = (Exception, SomethingBadHappened)
    # A boolean, or a number. If this option is set to True, autoretries will be delayed following the rules of exponential backoff.
    retry_backoff=True
    # Set to none to repeat the task ongingly.
    max_retries=None    

    rate_limit=f'{str(settings.coingecko_rate_limit_per_minute)}/m'

    @property
    def r(self) -> Redis:
        if self._redis is None:
            self._redis = Redis()
        return self._redis           

    @property
    def db(self) -> scoped_session:
        if self._db is None:
            self._db = ScopedSession()
        return self._db    

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
       pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))        
        
class APICallTask(Task):
    
    _db: scoped_session = None
    _redis: Redis
    
    rate_limit=f'{str(settings.coingecko_rate_limit_per_minute)}/m'
    
    @property
    def r(self) -> Redis:
        if self._redis is None:
            self._redis = Redis()
        return self._redis           
    
    @property
    def db(self) -> scoped_session:
        if self._db is None:
            self._db = ScopedSession()
        return self._db           

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))           
        
        
class RpcCallTask(Task):
            
    _db: scoped_session = None
    _redis: Redis
    
    abstract = True
    # retries the task on the Exceptions it can be customized to raise Exceptions based on unwanted results
    autoretry_for = (Exception, SomethingBadHappened)
    # A boolean, or a number. If this option is set to True, autoretries will be delayed following the rules of exponential backoff.
    retry_backoff=True
    # Set to none to repeat the task ongingly.
    max_retries=None    

    rate_limit=f'{str(settings.general_rpc_call_rate_limit_per_minute)}/m'

    @property
    def r(self) -> Redis:
        if self._redis is None:
            self._redis = Redis()
        return self._redis           

    @property
    def db(self) -> scoped_session:
        if self._db is None:
            self._db = ScopedSession()
        return self._db    

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
       pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))                

class Workflow_Task(Task):
    
    _db: scoped_session = None

    @property
    def db(self) -> scoped_session:
        if self._db is None:
            self._db = ScopedSession()
        return self._db    

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        
       pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))        
