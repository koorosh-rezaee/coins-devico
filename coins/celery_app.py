from celery import Celery
from kombu import Queue
from coins.core.config import settings

app = Celery('celery-worker',
             broker=settings.celery_broker_url,
             backend=settings.celery_backend_url,
             )

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=36000,
)


app.control.rate_limit('coins.tasks.api_call_tasks.#', '1/m')

app.conf.task_queues = (
    Queue('celery'),
    Queue('crud-queue'),
    Queue('api-call-queue'),
    Queue('high-priority-queue'),
)



# app.conf.update(
#     task_routes = {
        
#         # registers tasks in the celery_test.slow_tasks.tasks.py to be sent to slow-queue
#         'celery_test.tasks.slow_tasks.tasks.*': {'queue': 'slow-queue'},
#     },
# )

# every worker is allowed to pick one task at a time before the another is acknowleged
app.conf.update(worker_prefetch_multiplier = 1,)

# when a worker crashes or gets shutdown the task will be re-queued and another wother picks it up
app.conf.update(task_acks_late = True,)

# task discovery registers tasks in the config
app.autodiscover_tasks([
        'coins.tasks'
        ])

if __name__ == '__main__':
    app.start()