import datetime
import pytz

from apps.account.models import Participant
from apps.notifications.models import Notification
from project.celery import app


@app.task
def send_task_for_participant():
    participants = Participant.objects.all()

    for participant in participants:
        date_time = participant.get_participant_time()
        task = participant.get_today_task()
        if task:
            Notification.task_today(participant, date_time, task)
        # if date.hour == 0:
        #     pass


