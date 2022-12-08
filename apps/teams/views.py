from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from apps.account.models import Participant
from apps.teams.forms import AddDesireForm
from apps.teams.models import DesiredTeam, Team, TeamParticipant


@login_required
@require_http_methods(['POST'])
def add_desire(request):
    if request.method == 'POST' and 'window' in request.POST:
        if request.POST['window'] == 'open':
            return open_add_desire_form(request)
        if request.POST['window'] == 'form':
            return send_add_desire_form(request)


def open_add_desire_form(request):
    context = {
        'window': 'form',
    }

    add_desire_window = render_to_string('teams/popups/add_desire.html', context, request)

    out = {
        'status': 'ok',
        'action': 'window',
        'window': add_desire_window,
    }

    return JsonResponse(out)


def send_add_desire_form(request):
    form = AddDesireForm(request.POST)

    if form.is_valid():
        phone = form.cleaned_data['phone']

        try:
            desired_participant = Participant.objects.get(phone=phone)

            DesiredTeam.objects.create(desirer=request.user.participant, desired_participant=desired_participant)

            context = {
                'window': 'successful',
                'reload_overlay': True
            }

            add_desire_window = render_to_string('teams/popups/add_desire.html', context, request)

        except ObjectDoesNotExist:
            context = {
                'window': 'form',
                'errors': {
                    'phone': 'Участника с таким телефоном не найдено'
                }
            }

            add_desire_window = render_to_string('teams/popups/add_desire.html', context, request)

    else:
        context = {
            'window': 'form',
            'errors': form.errors
        }

        add_desire_window = render_to_string('teams/popups/add_desire.html', context, request)

    out = {
        'status': 'ok',
        'action': 'window',
        'window': add_desire_window,
    }

    return JsonResponse(out)


def index(request):
    desire_list = DesiredTeam.objects.filter(desirer=request.user.participant)

    context = {
        'desire_list': desire_list,
        'current_karathon_team': current_karathon_team(request)
    }

    return render(request, 'teams/team.html', context)


def current_karathon_team(request):
    active_karathon = request.user.participant.get_active_karathon()
    try:
        team = Team.objects.get(karathon=active_karathon, teamparticipant__participant=request.user.participant)
        team.team_participants = TeamParticipant.objects.filter(team=team).exclude(participant=request.user.participant)
        return team
    except ObjectDoesNotExist:
        return None


