# Import the Flask app FIRST so ContextTask is registered
import app

# Then import the Celery instance
from celery_config import celery

# Finally register all tasks
import tasks