from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import json

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
            desired_participant = get_object_or_404(Participant, phone=phone)
            if request.user.participant == desired_participant:
                context = {
                    'window': 'form',
                    'errors': '* Ты не можешь добавить себя в команду',
                }
                add_desire_window = render_to_string('teams/popups/add_desire.html', context, request)
                out = {
                    'status': 'ok',
                    'action': 'window',
                    'window': add_desire_window,
                }
                return JsonResponse(out)
            if DesiredTeam.objects.filter(desirer=request.user.participant, desired_participant=desired_participant).exists():
                error_text = '* {} уже в твоей команде, выбери кого-то ещё'.format(desired_participant.first_name)
                context = {
                    'window': 'form',
                    'errors': error_text,
                }
                add_desire_window = render_to_string('teams/popups/add_desire.html', context, request)
                out = {
                    'status': 'ok',
                    'action': 'window',
                    'window': add_desire_window,
                }
                return JsonResponse(out)
            
            
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
    if request.method == 'POST':
        return delete_user(request)
    desire_list = DesiredTeam.objects.select_related().filter(desirer__user=request.user.participant)
    context = {
        'desire_list': desire_list,
        'current_karathon_team': current_karathon_team(request),
    }
    return render(request, 'teams/team.html', context)

def delete_user(request):
    id_user_to_delete = json.loads(request.body).get("user_id")
    get_object_or_404(DesiredTeam, id=id_user_to_delete).delete()
    out = {
        'status': 'ok',
    }
    return JsonResponse(out)

def current_karathon_team(request):
    active_karathon = request.user.participant.get_active_karathon()
    try:
        team = Team.objects.get(karathon=active_karathon, teamparticipant__participant=request.user.participant)
        team.team_participants = TeamParticipant.objects.filter(team=team).exclude(participant=request.user.participant)
        return team
    except ObjectDoesNotExist:
        return None


