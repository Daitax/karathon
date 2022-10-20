import datetime
import pytz

from apps.account.models import Participant
from project.celery import app


@app.task
def send_task_for_participant():
    participants = Participant.objects.all()

    for participant in participants:
        date = participant.get_participant_time()
        if date.hour == 0:
            pass
