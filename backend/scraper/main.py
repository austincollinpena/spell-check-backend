from backend.utils.celery_worker_module.celery_worker import celery_worker


@celery_worker.task
def hello_from_the_other_module():
    return 'hello world!'
