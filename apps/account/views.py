import datetime
import json
from random import randint

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView

from apps.core.utils import ending_numbers
from apps.notifications.models import Notification
from apps.steps.models import Step
from apps.teams.models import Team, TeamParticipant

from .forms import (
    AuthCodeForm,
    AuthEmailForm,
    ParticipantForm,
    WinnerQuestionnaireForm,
)
from .models import Participant, EmailCode, Winner, WinnerQuestionnaire


class AuthView(TemplateView):
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and "window" in request.POST:
            if request.POST["window"] == "open":
                return self.open_popup(request)
            if request.POST["window"] == "email":
                return self.auth_phone(request)
            if request.POST["window"] == "code":
                return self.auth_code(request)

    def open_popup(self, request):
        context = {
            "window": "email",
        }
        auth_window = render_to_string(
            "account/popups/authentication.html", context, request
        )
        out = {
            "status": "ok",
            "action": "window",
            "window": auth_window,
        }
        return JsonResponse(out)

    def auth_phone(self, request):
        form = AuthEmailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            # code = randint(1000, 9990)
            code = 1234
            sending_code = EmailCode.send_code(email, code)

            if sending_code["status"] == "ok":
                context = {
                    "window": "code",
                    "email": email
                }

                auth_window = render_to_string(
                    "account/popups/authentication.html", context, request
                )

                out = {
                    "status": "ok",
                    "action": "window",
                    "window": auth_window,
                }

                response = JsonResponse(out)
                EmailCode.set_cookie_code(response, code)
                EmailCode.set_cookie_attempts(response, 3)
                return response
            else:
                form.add_error('email', 'Ошибка отправки сообщения')

                context = {
                    "window": "email",
                    "email": email,
                    "errors": form.errors,
                }
        else:
            email_input = form['email'].value()
            context = {
                "window": "email",
                "email": email_input,
                "errors": form.errors
            }

        auth_window = render_to_string(
            "account/popups/authentication.html", context, request
        )

        out = {
            "status": "ok",
            "action": "window",
            "window": auth_window,
        }

        return JsonResponse(out)

    def auth_code(self, request):
        if not "attempts" in request.COOKIES:
            return self.open_popup(request)

        form = AuthCodeForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            code = form.cleaned_data["code"]

            is_code_correct = EmailCode.check_code(request, code)

            if is_code_correct:
                try:
                    participant = Participant.objects.get(email=email)
                    login(request, participant)

                    out = {
                        "status": "ok",
                        "action": "reload",
                    }

                    return JsonResponse(out)
                except ObjectDoesNotExist:
                    new_participant = Participant.objects.create_user(
                        username=email,
                        email=email,
                    )

                    login(request, new_participant)

                    context = {"window": "enter", "reload_overlay": True}
            else:
                attempts = EmailCode.login_attempts(request)

                if attempts == 1:
                    return self.open_popup(request)
                else:
                    form.add_error('code', 'Неверный код. Осталось попыток {} '.format(attempts - 1))

                    context = {
                        "window": "code",
                        "email": email,
                        "code": code,
                        "errors": form.errors,
                    }

                    auth_window = render_to_string(
                        "account/popups/authentication.html", context, request
                    )

                    out = {
                        "status": "ok",
                        "action": "window",
                        "window": auth_window,
                    }
                    response = JsonResponse(out)

                    EmailCode.set_cookie_attempts(response, attempts - 1)

                    return response

        else:
            context = {"window": "code", "errors": form.errors}

        auth_window = render_to_string(
            "account/popups/authentication.html", context, request
        )

        out = {
            "status": "ok",
            "action": "window",
            "window": auth_window,
        }

        return JsonResponse(out)


@login_required
def index(request):
    participant_form = ParticipantForm(instance=request.user.participant)
    if request.method == "POST" and "personal" in request.POST:
        participant_form = ParticipantForm(
            request.POST, request.FILES, instance=request.user.participant
        )

        if participant_form.is_valid():
            participant_form.save()
            participant_form = ParticipantForm(
                instance=request.user.participant
            )

    context = {
        "participant_form": participant_form,
    }

    if WinnerQuestionnaire.is_active_questionnaire(request.user.participant):
        winner_questionnaire = WinnerQuestionnaire.objects.get(
            is_displayed=True,
            participant=request.user.participant
        )
        winner_questionnaire_form = WinnerQuestionnaireForm(instance=winner_questionnaire)

        if request.method == 'POST' and 'winner' in request.POST:
            winner_questionnaire_form = WinnerQuestionnaireForm(
                request.POST, instance=winner_questionnaire
            )
            if winner_questionnaire_form.is_valid():
                winner_questionnaire_form.save()
                winner_questionnaire_form = WinnerQuestionnaireForm(instance=winner_questionnaire)

        context['winner_questionnaire_form'] = winner_questionnaire_form

    return render(request, "account/index.html", context)


@login_required(login_url="core:site-index")
def messages(request):
    if request.method == "POST":
        return messages_read(request)
    if request.method == "GET_PREV_MESSAGES":
        return messages_add(request)
    user = request.user.participant
    messages_list = Notification.objects.select_related("participant").filter(
        participant__user=user,
        is_viewed=False,
    )
    if len(messages_list) <= settings.MESSAGES_PER_PAGE:
        messages_list = Notification.objects.select_related(
            "participant"
        ).filter(participant__user=user, )[: settings.MESSAGES_PER_PAGE]
    return render(
        request,
        "account/messages.html",
        {
            "messages_list": messages_list,
            "next_messages_exist": Notification(
                participant=user
            ).next_page_exists(),
        },
    )


def messages_add(request):
    messages_list = Notification.objects.select_related("participant").filter(
        participant__user=request.user.participant,
    )
    messages_showed = list(json.loads(request.body).values())[0]
    if messages_showed + settings.MESSAGES_PER_PAGE < len(messages_list):
        messages_list = messages_list[
                        messages_showed: messages_showed + settings.MESSAGES_PER_PAGE
                        ]
        next_messages_exist = True
    messages_list = messages_list[messages_showed:]
    next_messages_exist = False
    context = {
        "messages_list": messages_list,
    }
    messages_block = render_to_string(
        "account/includes/messages_block.html", context, request
    )
    out = {
        "status": "ok",
        "messages_block": messages_block,
        "next_messages_exist": next_messages_exist,
    }
    return JsonResponse(out)


def messages_read(request):
    data = json.loads(request.body)
    mes_showed = data.pop("amount")
    messages_ids = list(data.values())
    messages_to_update = [
        get_object_or_404(Notification, id=message_id)
        for message_id in messages_ids
    ]
    for message in messages_to_update:
        message.is_viewed = True
    Notification.objects.bulk_update(messages_to_update, ["is_viewed"])
    messages_list = Notification.objects.select_related("participant").filter(
        participant__user=request.user.participant,
    )[:mes_showed]
    context = {
        "messages_list": messages_list,
    }
    messages_block = render_to_string(
        "account/includes/messages_block.html", context, request
    )
    out = {
        "status": "ok",
        "messages_block": messages_block,
    }
    return JsonResponse(out)


class ResultsView(LoginRequiredMixin, TemplateView):
    template_name = "account/results.html"
    login_url = "/"

    def get_context_data(self, **kwargs):
        words = ["шаг", "шага", "шагов"]
        context = super().get_context_data(**kwargs)

        # Получаем активный карафон
        active_karathon = self.request.user.participant.get_active_karathon()

        if active_karathon:
            participant_karathon_steps = []  # Список шагов по дням
            total = 0  # Итоговое количество шагов
            total_team = 0  # Итоговое количество шагов у команды

            # Если тип карафона - командный
            if active_karathon.type == "team":
                team = Team.objects.get(
                    teamparticipant__participant=self.request.user.participant,
                    karathon=active_karathon
                )
                # Собираем ID всех участников команды
                team_participants_id = TeamParticipant.objects.filter(team=team).values_list('participant', flat=True)

            # Определяем дату начала карафона
            date_start_karathon = active_karathon.starts_at

            # Определяем дату, до которой отображаем список в результатах
            if active_karathon.is_ended_karathon():
                date_end = active_karathon.finished_at
            else:
                date_end = self.request.user.participant.get_participant_time().date()

            date = date_start_karathon

            # Проходим цикл по каждому дню
            while date <= date_end:

                # Если в текущем дне есть отчёт по шагам
                try:
                    step = Step.objects.get(
                        date=date,
                        participant=self.request.user.participant,
                        karathon=active_karathon
                    )
                    # Добавляем его и плюрализацию
                    steps_data = [step, ending_numbers(step.steps, words)]

                    # Суммируем с персональным итоговым количеством
                    total += step.steps

                except ObjectDoesNotExist:
                    # Если нет, то передаём пустой элемент с датой
                    steps_data = [None, date]

                # Если тип карафона "Командный"
                if active_karathon.type == "team":

                    # Получаем сумму шагов всех участников за текущий день
                    team_steps = Step.objects.filter(
                        date=date,
                        karathon=active_karathon,
                        participant__in=team_participants_id
                    ).aggregate(Sum("steps"))['steps__sum']

                    # Суммируем с командным итоговым количеством
                    total_team += team_steps if team_steps else 0

                    # Добавляем в массив дня
                    steps_data.append(team_steps)

                    # Если за текущий день есть отчёты, то добавлям плюрализацию
                    if team_steps:
                        steps_data.append(ending_numbers(team_steps, words))

                # Добавляем данные в массив вывода по дням
                participant_karathon_steps.append(steps_data)
                # Переходим на следующую итерацию (день)
                date += datetime.timedelta(days=1)

            # Заполняем массив вывода суммы шагов
            output_total_karathon_steps = [
                total,
                ending_numbers(total, words)
            ]
            # Если тип карафона "Командный"
            if active_karathon.type == "team":
                # Добавляем массив вывода суммы шагов командными значениями
                output_total_karathon_steps.append(total_team)
                output_total_karathon_steps.append(ending_numbers(total_team, words))

            # Выводим данные в шаблон
            context["steps"] = reversed(participant_karathon_steps)
            context["total"] = output_total_karathon_steps

        context["karathon"] = active_karathon

        return context
