from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from .forms import ReportForm
from .models import Step
from ..core.utils import send_email_message
from ..notifications.models import Notification
from ..tasks.models import Task


@login_required
@require_http_methods(["POST"])
def add_report(request):
    if request.method == "POST" and "window" in request.POST:
        if request.POST["window"] == "open":
            return open_report_form(request)
        if request.POST["window"] == "form":
            return send_report_form(request)
        if request.POST["window"] == "open-change":
            return open_change_report_form(request)
        if request.POST["window"] == "form-change":
            return send_change_report_form(request)


def open_report_form(request):
    context = {
        "window": "form",
    }

    report_window = render_to_string(
        "steps/popups/report.html", context, request
    )

    out = {
        "status": "ok",
        "action": "window",
        "window": report_window,
    }

    return JsonResponse(out)


def send_report_form(request):
    form = ReportForm(request.POST, request.FILES)

    if form.is_valid():
        steps = form.cleaned_data["steps"]
        photo = form.cleaned_data["photo"]

        date = request.user.participant.get_participant_time()
        karathon = request.user.participant.get_active_karathon()

        is_today_report = request.user.participant.is_today_report()

        if is_today_report:
            context = {
                "window": "form",
                "errors": {"report": "Сегодня отчёт уже сдан"},
            }

            report_window = render_to_string(
                "steps/popups/report.html", context, request
            )

            out = {
                "status": "ok",
                "action": "window",
                "window": report_window,
            }

            return JsonResponse(out)

        else:
            # if settings.IS_NEED_CHECK_STEPS:
            #     if not Step().amount_matches_screenshot(
            #         participant=request.user,
            #         photo=photo,
            #         steps=steps,
            #     )[0]:
            #         with open(
            #             "karathon/apps/steps/static/steps/checking_convertation.txt",
            #             "a+",
            #         ) as checking_file:
            #             screenshot_steps = Step().amount_matches_screenshot(
            #                 participant=request.user,
            #                 photo=photo,
            #                 steps=steps,
            #             )[1]
            #             checking_file.write(
            #                 "внёс пользователь {} || "
            #                 "считано со скриншота {} || "
            #                 "фото {}"
            #                 "\n------------------------------------------ \n".format(
            #                     steps, screenshot_steps, photo
            #                 )
            #             )
            create_report = Step.objects.create(
                date=date,
                participant=request.user,
                steps=steps,
                photo=photo,
                karathon=karathon,
            )

            if Task.is_task_completed(create_report):
                create_report.bonus = request.user.participant.today_task().bonus
                create_report.is_completed = True
                create_report.save()
                Notification.notification_from_template(request.user.participant, 'task_completed')
                context = {
                    "window": "task_completed", "reload_overlay": True
                }
            else:
                create_report.bonus = None
                create_report.is_completed = False
                create_report.save()
                Notification.notification_from_template(request.user.participant, 'task_not_completed')
                send_email_message(
                    'Задание дня не выполнено!',
                    'Но у тебя ещё есть шанс его выполнить до конца дня, изменив отчёт',
                    request.user.participant.email
                )
                context = {
                    "window": "task_not_completed", "reload_overlay": True
                }

            report_window = render_to_string(
                "steps/popups/report.html", context, request
            )

    else:
        context = {"window": "form", "errors": form.errors}

        report_window = render_to_string(
            "steps/popups/report.html", context, request
        )

    out = {
        "status": "ok",
        "action": "window",
        "window": report_window,
    }

    return JsonResponse(out)

def open_change_report_form(request):
    participant = request.user.participant
    participant_date = participant.get_participant_time().date()
    karathon = request.user.participant.get_active_karathon()

    sent_report = Step.objects.get(
        date=participant_date,
        participant=participant,
        karathon=karathon,
    )

    context = {
        "window": "form-change",
        "sent_report_steps": sent_report.steps
    }

    report_window = render_to_string(
        "steps/popups/change_report.html", context, request
    )

    out = {
        "status": "ok",
        "action": "window",
        "window": report_window,
    }

    return JsonResponse(out)

def send_change_report_form(request):
    form = ReportForm(request.POST, request.FILES)

    if form.is_valid():
        steps = form.cleaned_data["steps"]
        photo = form.cleaned_data["photo"]

        participant = request.user.participant
        participant_date = participant.get_participant_time().date()
        karathon = request.user.participant.get_active_karathon()

        report = Step.objects.get(
            date=participant_date,
            participant=participant,
            karathon=karathon,
        )

        report.steps = steps
        report.photo = photo
        report.save()

        if Task.is_task_completed(report):
            report.bonus = request.user.participant.today_task().bonus
            report.is_completed = True
            report.save()
            Notification.notification_from_template(request.user.participant, 'task_completed')
            context = {
                "window": "task_completed", "reload_overlay": True
            }
        else:
            report.bonus = None
            report.is_completed = False
            report.save()
            Notification.notification_from_template(request.user.participant, 'task_not_completed')
            send_email_message(
                'Задание дня не выполнено!',
                'Но у тебя ещё есть шанс его выполнить до конца дня, изменив отчёт',
                request.user.participant.email
            )
            context = {
                "window": "task_not_completed", "reload_overlay": True
            }

        report_window = render_to_string(
            "steps/popups/change_report.html", context, request
        )

    else:
        participant = request.user.participant
        participant_date = participant.get_participant_time().date()
        karathon = request.user.participant.get_active_karathon()

        sent_report = Step.objects.get(
            date=participant_date,
            participant=participant,
            karathon=karathon,
        )

        context = {
            "window": "form-change",
            "errors": form.errors,
            "sent_report_steps": sent_report.steps,
        }

        report_window = render_to_string(
            "steps/popups/change_report.html", context, request
        )

    out = {
        "status": "ok",
        "action": "window",
        "window": report_window,
    }

    return JsonResponse(out)
