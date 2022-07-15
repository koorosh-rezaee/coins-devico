from pydantic import AnyUrl, BaseSettings, RedisDsn, AmqpDsn


class Settings(BaseSettings):
    celery_broker_url: AmqpDsn
    celery_backend_url: RedisDsn
    
    postgresql_url: AnyUrl = "postgresql://postgres:POSTGRESPASSWORD@localhost/coins"
    db_connection_recycle_seconds: int = 3600 # recycle connections after one hour
    db_pool_size: int = 10 # when starting the worker how many db connections are created and added to the pool size  
    
    redis_url: AnyUrl = "redis://localhost:6379/15" # For prices
    
    coingecko_rate_limit_per_minute: int = 40 #
    coingecko_api_v3_base_url: str = "https://api.coingecko.com/api/v3"
    
    price_watcher_interval_seconds: int = 30 # sends an update task to fetch and update watched_for_price=True coins every x seconds
      
    class Config:
        env_file = '.env'
        
    
    
def get_settings():
    return Settings()

settings = get_settings()