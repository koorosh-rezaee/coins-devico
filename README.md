# coins-devico

## Caution

***be sure to install docker compose v2 first***
- `sudo apt-get install docker-compose-plugin`

## running the project

simply use:
- `./coins-start.sh`

## teardown

use this script:
- `./coins-stop.sh`

## API endpoints

After running the script an image of the project will be built under the name of coins-devoco and is added to your docker local registery
a web app and some celery apps get started along with redis postgresql and rabbitmq

***API docs are at: <http://localhost:80/docs>***

a short description about them:

***1- /update_coins_table***
    > to update the coins table so that we can fetch their contract addresses and decimals based on them later on
    > this api runs a task to fetch all coin ids and saves them to the db, ***be sure to run this first***


***2- /update_coins_contracts_table***
    > this will also run a huge number of tasks and enqueu them to be fetched one by one at a rate limit set in 
    > project_config>coins.env> coingecko_rate_limit_per_minute=<rate limit> this should be half the rate limit of the 
    > plan you are getting from coinsgeko because two celery workers are consuming tasks from a queue of this type
    >> after you run this task one time unless you set force=True, it will only return the progress about how much 
    >> token contracts it retrieved from the coingeko's api


***3- /update_coins_contracts_decimals_column***
    > right after all of the token contracts have been saved to the db you can call this api with the platform
    > parameter of your choice so that decimals of the contracts in the db which are of this platform get fetched
    > and saved to the db
    >> right now two platforms are supported by this test project *ethereum* and *BSC*


***4- /set_watch_for_price***
    > because of the rate limit and the timeout we might hit you should not set all of the coins to watch the prices for
    > and only set those you are interested in getting an update for
    >> after setting the coin to be watched for price every project_config>coins.env>price_watcher_interval_seconds seconds
    >> a task gets enqueued to make an api call to coinsgecko to fetch the latest price for these coins
    >> and you can fetch them later on by subscribing to a graphql subscription we will introduce later in this document
  
 
*** 5- /get_coin_ids***
    > at this end point you will recieve all of the possible coin_id values you could set to watch the prices for
  
  
*** 6- /get_watching_for_price_coin_ids***
    > and here you you can see what tokens have been set to watch the prices for
  
  
 ## GraphQL
  
  
