from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from .forms import AuthPhoneForm, AuthCodeForm, ParticipantForm
from .models import Participant, Sms
from apps.notifications.models import Notification


@require_http_methods(['POST'])
def authentication(request):
    if request.method == 'POST' and 'window' in request.POST:
        if request.POST['window'] == 'open':
            return open_auth(request)
        if request.POST['window'] == 'phone':
            return auth_phone(request)
        if request.POST['window'] == 'code':
            return auth_code(request)


def open_auth(request):
    context = {
        'window': 'phone',
    }

    auth_window = render_to_string('account/popups/authentication.html', context, request)

    out = {
        'status': 'ok',
        'action': 'window',
        'window': auth_window,
    }

    return JsonResponse(out)


def auth_phone(request):
    form = AuthPhoneForm(request.POST)

    if form.is_valid():
        phone = str(form.cleaned_data['phone'])
        # code = randint(1000, 9999)

        # TODO Раскомментировать проверку куков
        code = 1122
        # if not request.COOKIES.get('code'):
        sms_sending_response = Sms.send_code(phone, code)
        if sms_sending_response['status'] == 'OK':
            context = {
                'window': 'code',
                'phone': phone,
            }
            auth_window = render_to_string('account/popups/authentication.html', context, request)

            out = {
                'status': 'ok',
                'action': 'window',
                'window': auth_window,
            }

            response = JsonResponse(out)
            Sms.set_cookie_code(response, code)
            return response
        else:
            context = {
                'window': 'phone',
                'phone': phone,
                'errors': {
                    'code': 'Ошибка отправки СМС'
                }
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
        context = {
            'window': 'phone',
            'errors': form.errors
        }

    auth_window = render_to_string('account/popups/authentication.html', context, request)

    out = {
        'status': 'ok',
        'action': 'window',
        'window': auth_window,
    }

    return JsonResponse(out)


def auth_code(request):
    form = AuthCodeForm(request.POST)

    if form.is_valid():
        phone = str(form.cleaned_data['phone'])
        code = form.cleaned_data['code']

        is_code_correct = Sms.check_code(request, code)
        if is_code_correct:
            try:
                participant = Participant.objects.get(phone=phone)
                login(request, participant)

                out = {
                    'status': 'ok',
                    'action': 'reload',
                }

                return JsonResponse(out)
            except ObjectDoesNotExist:
                new_participant = Participant.objects.create_user(
                    username=phone,
                    phone=phone,
                )
                login(request, new_participant)

                context = {
                    'window': 'enter',
                    'reload_overlay': True
                }
        else:
            context = {
                'window': 'code',
                'phone': phone,
                'code': code,
                'errors': {
                    'code': '* Введён неправильный СМС код'
                }
            }
    else:
        context = {
            'window': 'code',
            'errors': form.errors
        }

    auth_window = render_to_string('account/popups/authentication.html', context, request)

    out = {
        'status': 'ok',
        'action': 'window',
        'window': auth_window,
    }

    return JsonResponse(out)


def index(request):
    participant_form = ParticipantForm(instance=request.user.participant)
    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST, request.FILES, instance=request.user.participant)

        if participant_form.is_valid():
            participant_form.save()
            participant_form = ParticipantForm(instance=request.user.participant)

    return render(request, 'account/index.html', {'participant_form': participant_form})


def messages(request):
    messages_list = Notification.objects.filter(participant=request.user.participant)
    return render(request, 'account/messages.html', {
        'messages_list': messages_list,
    })


def results(request):
    context = {}
    return render(request, 'account/results.html', context)


def user_logout(request):
    logout(request)
    return redirect('core:site-index')