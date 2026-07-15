from celery import Celery

celery = Celery("placement_portal")

celery.conf.update(

    broker_url="redis://localhost:6379/0",

    result_backend="redis://localhost:6379/0",

    timezone="Asia/Kolkata",

    enable_utc=False

)