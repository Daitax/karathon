from project.celery import app


@app.task
def send_task_for_participant():
    from apps.account.models import Participant
    participants = Participant.objects.all()

    for participant in participants:
        date_time = participant.get_participant_time()
        task = participant.today_task()
        if task and date_time.hour == 0:
            from apps.notifications.models import Notification
            Notification.task_today(participant, date_time, task)


def send_notification_add_instagram(participant):
    from apps.notifications.models import Notification
    Notification.notification_from_template(participant, "link_to_instagram")


# def send_notification_add_email(participant):
#     from apps.notifications.models import Notification
#     Notification.notification_from_template(participant, "link_to_email")

def send_notification_add_phone(participant):
    from apps.notifications.models import Notification
    Notification.notification_from_template(participant, "link_to_phone")
