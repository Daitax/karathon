import datetime

from django.core.exceptions import ObjectDoesNotExist

from apps.core.utils import send_email_message, format_date
from apps.notifications.models import Notification
from project.celery import app


@app.task
def uncompleted_task():
    from apps.account.models import Participant
    from apps.account.models import ParticipantsKarathon
    from apps.steps.models import Step
    from apps.tasks.models import Task
    participants = Participant.objects.all()

    for participant in participants:
        active_karathon = participant.get_active_karathon()
        if active_karathon:
            date_time = participant.get_participant_time()
            if date_time.hour == 23:
                try:
                    report = Step.objects.get(
                        date=date_time.date(),
                        participant=participant,
                    )

                    if not Task.is_task_completed(report):
                        # Тут отправляем оповещение о необходимости выполнить задание
                        Notification.notification_from_template(participant, 'warning_task_not_completed')
                        send_email_message(
                            'Напоминание о задании за ' + format_date(report.date),
                            'Твоё задание на день не выполнено. Последний час для выполнения задания!',
                            participant.email
                        )


                except ObjectDoesNotExist:
                    # Тут отправляем оповещение о необходимости сдать отчёт и выполнить задание
                    Notification.notification_from_template(participant, 'warning_report_not_send')
                    send_email_message(
                        'Напоминание о задании',
                        'Ты сегодня ещё не отправил отчёт с выполненным заданием. Поторопись! Остался час!',
                        participant.email
                    )

            if date_time.hour == 0:
                try:
                    report = Step.objects.get(
                        date=date_time.date() - datetime.timedelta(days=1),
                        participant=participant,
                    )

                    if not Task.is_task_completed(report):
                        # Тут удаляем участника из карафона
                        Notification.notification_from_template(participant, 'task_not_completed_del')
                        send_email_message(
                            'Исключение из карафона',
                            'Упс, ты молодец, но для тебя задание оказалось слишком сложным. На этом твое участие'
                            ' в этом карафоне завершено, но я жду тебя в следующем!',
                            participant.email
                        )
                        ParticipantsKarathon.do_karathon_exclusion(participant, karathon=active_karathon)

                except ObjectDoesNotExist:
                    # Тут удаляем участника из карафона
                    Notification.notification_from_template(participant, 'report_not_send_del')
                    send_email_message(
                        'Исключение из карафона',
                        'Приветик! Я везде искала, но так и не смогла найти твой отчет за вчерашний день.'
                        ' На этом твое участие в этом карафоне завершено, но я жду тебя в следующем!',
                        participant.email
                    )
                    ParticipantsKarathon.do_karathon_exclusion(participant, karathon=active_karathon)
