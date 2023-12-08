import datetime
import json
import os

from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_list_or_404, render
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView

from apps.account.models import Participant
from apps.core.models import Karathon

from apps.core.yookassa import create_payment, confirmation_payment
from apps.steps.models import Step


def index(request):
    try:
        presentation_karathon = Karathon.objects.get(is_presentation=True)

        context = {"presentation_karathon": presentation_karathon}

    except ObjectDoesNotExist:
        context = {}

    return render(request, "core/index.html", context)


class ChampionsView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET_CHAMPS_LIST":
            return self.add_champs_list(request)
        if request.method == "GET":
            return self.champions(request)

    def add_champs_list(self, request):
        data = json.loads(request.body)
        champs_showed = data.pop("amount_champs")
        champ_list = Step.get_champs_list()
        next_champs_exist = True

        champs_to_show = champs_showed + 3 + 4

        champs_block = render_to_string(
            "core/includes/champs_page_block.html",
            {
                "other_champs": champ_list[3:champs_to_show]
            },
            request,
        )

        if champs_to_show >= len(champ_list):
            next_champs_exist = False
        out = {
            "status": "ok",
            "champs_showed": champs_showed,
            "champs_block": champs_block,
            "next_champs_exist": next_champs_exist,
        }

        return JsonResponse(out)

    def champions(self, request):
        champ_list = Step.get_champs_list()

        top_champs = champ_list[:3]

        other_champs = champ_list[3:7]

        context = {
            'top_champs': top_champs,
            'other_champs': other_champs
        }

        return render(request, "core/champions.html", context)


def add_champs_list(request):
    data = json.loads(request.body)
    champs_showed = data.pop("amount_champs")
    more_champs = get_list_or_404(Participant)
    more_champs_list = []
    i = 0
    for ch in more_champs:
        more_champs_list.append([ch, i + 1])
        i += 1
    champs_to_show = (
        champs_showed
        + settings.CHAMPS_ON_FIRST_SCREEN
        + settings.CHAMPS_ADDITION
    )
    champs_block = render_to_string(
        "core/includes/champs_page_block.html",
        {
            "champs_rest": more_champs_list[
                settings.CHAMPS_ON_FIRST_SCREEN : champs_to_show
            ]
        },
        request,
    )
    next_champs_exist = True
    if champs_to_show >= len(more_champs):
        next_champs_exist = False
    out = {
        "status": "ok",
        "champs_showed": champs_showed,
        "champs_block": champs_block,
        "next_champs_exist": next_champs_exist,
    }
    return JsonResponse(out)


class KarathonView(TemplateView):
    template_name = "core/karathon.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        karathon_number = kwargs["karathon_number"]
        karathon = Karathon.objects.get(number=karathon_number)
        context = {
            "karathon": karathon,
            "request_url": self.request.path
        }
        return context


class PastKarathonsView(TemplateView):
    template_name = "core/past_karathons.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        past_karathons = Karathon.objects.filter(
            finished_at__lt=datetime.datetime.now() + datetime.timedelta(days=1)
        ).order_by('-finished_at')

        context = {
            "past_karathons": past_karathons,
        }
        return context

# class ParticipateView(LoginRequiredMixin, TemplateView, CreateView):
#     template_name = "core/participate.html"
#     login_url = "/"

#     def dispatch(self, request, *args, **kwargs):
#         if request.method == "POST":
#             karathon_id = self.request.POST["karathon"]
#             request.user.participant.karathon.add(karathon_id)

#     # def create_participant_karathon(self):

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         participant_date = self.request.user.participant.get_participant_time()
#         karathon_list = Karathon.objects.filter(
#             starts_at__gte=participant_date
#         )
#         participant_karathon_list = karathon_list.filter(
#             participant=self.request.user.participant
#         )
#         free_karathon_list = karathon_list.exclude(
#             participant=self.request.user.participant
#         )
#         intersecting_carathons_ids = []
#         for participant_karathon_item in participant_karathon_list:
#             for free_karathon_item in free_karathon_list:
#                 latest_start = max(
#                     free_karathon_item.starts_at,
#                     participant_karathon_item.starts_at,
#                 )
#                 earliest_end = min(
#                     free_karathon_item.finished_at,
#                     participant_karathon_item.finished_at,
#                 )
#                 if latest_start <= earliest_end:
#                     intersecting_carathons_ids.append(free_karathon_item.id)
#         available_karathon_list = free_karathon_list.exclude(
#             id__in=intersecting_carathons_ids
#         )
#         context = {
#             "participant_karathon_list": participant_karathon_list,
#             "available_karathon_list": available_karathon_list,
#         }
#         return context


def create_payment_link(data, participant):
    karathon_id = data['karathon_id']
    karathon_number = data['karathon_number']
    # email = data['email']
    email = participant.email
    link = ''
    try:
        karathon = Karathon.objects.get(id=karathon_id, number=karathon_number)

        # if data['payment_type'] == 'card':
        #     payment = create_payment(karathon, email, participant)
        #     link = payment.confirmation.confirmation_url
        # elif data['payment_type'] == 'paypal':
        #     pass
        payment = create_payment(karathon, email, participant)
        link = payment.confirmation.confirmation_url

    except ObjectDoesNotExist:
        raise Http404

    return link

@login_required
def participate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        out = {
            "status": "error",
        }

        if 'window' in data:
            if data['window'] == 'email':
                context = {
                    "window": data['window'],
                    "karathon_number": data['karathon_number'],
                    "karathon_id": data['karathon_id']
                }

            if data['window'] == 'type':
                context = {
                    "window": data['window'],
                    "karathon_number": data['karathon_number'],
                    "karathon_id": data['karathon_id'],
                    "email": data['email'],
                }

            if data['window'] == 'link':
                participant = request.user.participant
                link = create_payment_link(data, participant)

                context = {
                    "window": data['window'],
                    "link": link,
                }

            type_window = render_to_string(
                "core/popups/payment.html", context, request
            )

            out = {
                "status": "ok",
                "window": type_window,
            }

        return JsonResponse(out)

        # if "karathon" in request.POST:
            # karathon_id = request.POST["karathon"]
            # karathon = Karathon.objects.get(id=karathon_id)
            # participant = request.user.participant
            # payment = create_payment(karathon, participant)
            # payment_link = payment.confirmation.confirmation_url
            # request.user.participant.karathon.add(karathon_id)

    participant_date = request.user.participant.get_participant_time()

    karathon_list = Karathon.objects.filter(starts_at__gte=participant_date)

    participant_karathon_list = karathon_list.filter(
        participant=request.user.participant
    )
    free_karathon_list = karathon_list.exclude(
        participant=request.user.participant
    )
    intersecting_carathons_ids = []

    for participant_karathon_item in participant_karathon_list:
        for free_karathon_item in free_karathon_list:
            latest_start = max(
                free_karathon_item.starts_at,
                participant_karathon_item.starts_at,
            )
            earliest_end = min(
                free_karathon_item.finished_at,
                participant_karathon_item.finished_at,
            )

            if latest_start <= earliest_end:
                intersecting_carathons_ids.append(free_karathon_item.id)

    available_karathon_list = free_karathon_list.exclude(
        id__in=intersecting_carathons_ids
    )

    context = {
        "participant_karathon_list": participant_karathon_list,
        "available_karathon_list": available_karathon_list,
    }

    return render(request, "core/participate.html", context)


def webhooks_yookassa(request):
    event_json = json.loads(request.body)
    payment = confirmation_payment(event_json)

    return HttpResponse(status=200)


def webhooks_paypal(request):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'paypal.txt')  # full path to text.
    my_file = open(file_path, 'w+')

    my_file.write(str(request.__dict__))
    my_file.write('\n')
    my_file.write(str(request.body))
    my_file.write('\n')
    my_file.write(str(request.POST))
    my_file.write('\n')
    my_file.write(str(request.GET))
    my_file.write('\n')
    my_file.write('1234')
    my_file.close()

    return HttpResponse()


def csrf_failure(request, reason=""):
    return render(request, "core/403csrf.html")


def permission_denied(request, exception):
    return render(request, "core/403.html", status=403)


def page_not_found(request, exception):
    return render(request, "core/404.html", status=404)


def server_error(request):
    return render(request, "core/500.html", status=500)
