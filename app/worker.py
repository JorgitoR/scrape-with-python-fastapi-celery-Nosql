from celery import Celery
from . import config

celery_app =  Celery(__name__)
settings = config.get_setting()

REDIS_URL = settings.redis_url
celery_app.conf.broker_url     = REDIS_URL
celery_app.conf.result_backend = REDIS_URL

@celery_app.task
def random_task(name):
    print(f"Hello {name}")


"""
celery --app app.worker.celery_app worker --loglevel INFO

"""