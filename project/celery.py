import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'notification_about_uncompleted_task': {
        'task': 'apps.tasks.tasks.uncompleted_task',
        'schedule': crontab(hour='*', minute=0),
    },
    'send_tasks': {
        'task': 'apps.notifications.tasks.send_task_for_participant',
        'schedule': crontab(hour='*', minute=10),
    },
    'check_ending_karathons': {
        'task': 'apps.core.tasks.ended_karathon',
        'schedule': crontab(hour='*', minute=10),
    }
}
