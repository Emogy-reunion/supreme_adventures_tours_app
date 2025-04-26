from celery import Celery

def make_celery(app):
    celery = Celery(
            app.import_name,
            broker=app.config['CELERY_BROKER_URL'],
            backend=app.config['CELERY_BACKEND_URL']
            )
    celery.conf.update(app.config)
    return celery
