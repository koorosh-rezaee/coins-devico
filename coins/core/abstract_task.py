# misc imports
from celery import Task
from requests import Session
from sqlalchemy.orm.scoping import scoped_session

# app imports
from coins.core.custom_exceptions import SomethingBadHappened
from coins.models.database import ScopedSession
from coins.core.config import settings


class DBTask(Task):
        
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
        
        
class APICallTask(Task):
    
    _db: scoped_session = None
    
    rate_limit=f'{str(settings.coingecko_rate_limit_per_minute)}/m'

    @property
    def db(self) -> scoped_session:
        if self._db is None:
            self._db = ScopedSession()
        return self._db           

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
