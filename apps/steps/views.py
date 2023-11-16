from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from .forms import ReportForm
from .models import Step


@login_required
@require_http_methods(["POST"])
def add_report(request):
    if request.method == "POST" and "window" in request.POST:
        if request.POST["window"] == "open":
            return open_report_form(request)
        if request.POST["window"] == "form":
            return send_report_form(request)


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
            if settings.IS_NEED_CHECK_STEPS:
                if not Step().amount_matches_screenshot(
                    participant=request.user,
                    photo=photo,
                    steps=steps,
                )[0]:
                    with open(
                        "karathon/apps/steps/static/steps/checking_convertation.txt",
                        "a+",
                    ) as checking_file:
                        screenshot_steps = Step().amount_matches_screenshot(
                            participant=request.user,
                            photo=photo,
                            steps=steps,
                        )[1]
                        checking_file.write(
                            "внёс пользователь {} || "
                            "считано со скриншота {} || "
                            "фото {}"
                            "\n------------------------------------------ \n".format(
                                steps, screenshot_steps, photo
                            )
                        )
            Step.objects.create(
                date=date,
                participant=request.user,
                steps=steps,
                photo=photo,
                karathon=karathon,
            )

            context = {"window": "successful", "reload_overlay": True}

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
