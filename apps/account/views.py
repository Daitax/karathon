import json

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView

from apps.core.utils import ending_numbers
from apps.notifications.models import Notification
from apps.steps.models import Step

from .forms import (
    AuthCodeForm,
    AuthPhoneForm,
    ParticipantForm,
    WinnerQuestionnaireForm,
)
from .models import Participant, Sms, Winner


# @require_http_methods(["POST"])
# def authentication(request):
#     if request.method == "POST" and "window" in request.POST:
#         if request.POST["window"] == "open":
#             return open_auth(request)
#         if request.POST["window"] == "phone":
#             return auth_phone(request)
#         if request.POST["window"] == "code":
#             return auth_code(request)


# def open_auth(request):
#     context = {
#         "window": "phone",
#     }

#     auth_window = render_to_string(
#         "account/popups/authentication.html", context, request
#     )

#     out = {
#         "status": "ok",
#         "action": "window",
#         "window": auth_window,
#     }

#     return JsonResponse(out)


class AuthView(TemplateView):
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and "window" in request.POST:
            if request.POST["window"] == "open":
                return self.open_popup(request)
            if request.POST["window"] == "phone":
                return self.auth_phone(request)
            if request.POST["window"] == "code":
                return self.auth_code(request)

    def open_popup(self, request):
        context = {
            "window": "phone",
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
        form = AuthPhoneForm(request.POST)

        if form.is_valid():
            phone = str(form.cleaned_data["phone"])
            # code = randint(1000, 9999)

            # TODO Раскомментировать проверку куков
            code = 1122
            # if not request.COOKIES.get('code'):
            sms_sending_response = Sms.send_code(phone, code)
            if sms_sending_response["status"] == "OK":
                context = {
                    "window": "code",
                    "phone": phone,
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
                Sms.set_cookie_code(response, code)
                return response
            else:
                context = {
                    "window": "phone",
                    "phone": phone,
                    "errors": {"code": "Ошибка отправки СМС"},
                }
            # else:
            #     context = {
            #         'window': 'phone',
            #         'phone': phone,
            #         'errors': {
            #             'code': 'Повторная отправка СМС доступна через 1 минуту'
            #         }
            #     }
        else:
            context = {"window": "phone", "errors": form.errors}

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
        form = AuthCodeForm(request.POST)

        if form.is_valid():
            phone = str(form.cleaned_data["phone"])
            code = form.cleaned_data["code"]

            is_code_correct = Sms.check_code(request, code)
            if is_code_correct:
                try:
                    participant = Participant.objects.get(phone=phone)
                    login(request, participant)

                    out = {
                        "status": "ok",
                        "action": "reload",
                    }

                    return JsonResponse(out)
                except ObjectDoesNotExist:
                    new_participant = Participant.objects.create_user(
                        username=phone,
                        phone=phone,
                    )
                    login(request, new_participant)

                    context = {"window": "enter", "reload_overlay": True}
            else:
                context = {
                    "window": "code",
                    "phone": phone,
                    "code": code,
                    "errors": {"code": "* Введён неправильный СМС код"},
                }
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


# def auth_phone(request):
#     form = AuthPhoneForm(request.POST)

#     if form.is_valid():
#         phone = str(form.cleaned_data["phone"])
#         # code = randint(1000, 9999)

#         # TODO Раскомментировать проверку куков
#         code = 1122
#         # if not request.COOKIES.get('code'):
#         sms_sending_response = Sms.send_code(phone, code)
#         if sms_sending_response["status"] == "OK":
#             context = {
#                 "window": "code",
#                 "phone": phone,
#             }
#             auth_window = render_to_string(
#                 "account/popups/authentication.html", context, request
#             )

#             out = {
#                 "status": "ok",
#                 "action": "window",
#                 "window": auth_window,
#             }

#             response = JsonResponse(out)
#             Sms.set_cookie_code(response, code)
#             return response
#         else:
#             context = {
#                 "window": "phone",
#                 "phone": phone,
#                 "errors": {"code": "Ошибка отправки СМС"},
#             }
#         # else:
#         #     context = {
#         #         'window': 'phone',
#         #         'phone': phone,
#         #         'errors': {
#         #             'code': 'Повторная отправка СМС доступна через 1 минуту'
#         #         }
#         #     }
#     else:
#         context = {"window": "phone", "errors": form.errors}

#     auth_window = render_to_string(
#         "account/popups/authentication.html", context, request
#     )

#     out = {
#         "status": "ok",
#         "action": "window",
#         "window": auth_window,
#     }

#     return JsonResponse(out)


# def auth_code(request):
#     form = AuthCodeForm(request.POST)

#     if form.is_valid():
#         phone = str(form.cleaned_data["phone"])
#         code = form.cleaned_data["code"]

#         is_code_correct = Sms.check_code(request, code)
#         if is_code_correct:
#             try:
#                 participant = Participant.objects.get(phone=phone)
#                 login(request, participant)

#                 out = {
#                     "status": "ok",
#                     "action": "reload",
#                 }

#                 return JsonResponse(out)
#             except ObjectDoesNotExist:
#                 new_participant = Participant.objects.create_user(
#                     username=phone,
#                     phone=phone,
#                 )
#                 login(request, new_participant)

#                 context = {"window": "enter", "reload_overlay": True}
#         else:
#             context = {
#                 "window": "code",
#                 "phone": phone,
#                 "code": code,
#                 "errors": {"code": "* Введён неправильный СМС код"},
#             }
#     else:
#         context = {"window": "code", "errors": form.errors}

#     auth_window = render_to_string(
#         "account/popups/authentication.html", context, request
#     )

#     out = {
#         "status": "ok",
#         "action": "window",
#         "window": auth_window,
#     }

#     return JsonResponse(out)


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "account/index.html"
    login_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participant_form = ParticipantForm(
            instance=self.request.user.participant
        )
        if self.request.method == "POST" and "personal" in self.request.POST:
            participant_form = ParticipantForm(
                self.request.POST,
                self.request.FILES,
                instance=self.request.user.participant,
            )

            if participant_form.is_valid():
                participant_form.save()
                participant_form = ParticipantForm(
                    instance=self.request.user.participant
                )

        context = {
            "participant_form": participant_form,
        }

        # if Winner.is_winner_participant(request.user.participant):
        #     winner_questionnaire_form = WinnerQuestionnaireForm()
        #
        #     if request.method == 'POST' and 'winner' in request.POST:
        #         winner_questionnaire_form = WinnerQuestionnaireForm(request.POST)
        #
        #         if winner_questionnaire_form.is_valid():
        #             pass
        #
        #     context = {
        #         'participant_form': participant_form,
        #         'winner_questionnaire_form': winner_questionnaire_form
        #     }

        return context


# @login_required
# def index(request):
#     participant_form = ParticipantForm(instance=request.user.participant)
#     if request.method == "POST" and "personal" in request.POST:
#         participant_form = ParticipantForm(
#             request.POST, request.FILES, instance=request.user.participant
#         )

#         if participant_form.is_valid():
#             participant_form.save()
#             participant_form = ParticipantForm(
#                 instance=request.user.participant
#             )

#     context = {
#         "participant_form": participant_form,
#     }

#     # if Winner.is_winner_participant(request.user.participant):
#     #     winner_questionnaire_form = WinnerQuestionnaireForm()
#     #
#     #     if request.method == 'POST' and 'winner' in request.POST:
#     #         winner_questionnaire_form = WinnerQuestionnaireForm(request.POST)
#     #
#     #         if winner_questionnaire_form.is_valid():
#     #             pass
#     #
#     #     context = {
#     #         'participant_form': participant_form,
#     #         'winner_questionnaire_form': winner_questionnaire_form
#     #     }

#     return render(request, "account/index.html", context)


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
        ).filter(participant__user=user,)[: settings.MESSAGES_PER_PAGE]
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
            messages_showed : messages_showed + settings.MESSAGES_PER_PAGE
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
        participant_id = self.request.user.participant.id
        steps = Step.objects.filter(participant=participant_id)
        steps = [[item, ending_numbers(item.steps, words)] for item in steps]
        participant_steps = Step.objects.filter(
            participant=participant_id
        ).aggregate(Sum("steps"))
        participant_steps_total = [
            value for value in participant_steps.values()
        ][0]
        if not participant_steps_total:
            participant_steps_total = 0
        context = {
            "steps": steps,
            "participant_steps_total": [
                participant_steps_total,
                ending_numbers(participant_steps_total, words),
            ],
        }
        return context


# def user_logout(request):
#     logout(request)
#     return redirect("core:site-index")
