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

from apps.core.models import Karathon

from apps.core.yookassa import create_payment, confirmation_payment
from apps.steps.models import Step


def index(request):
    try:
        presentation_karathon = Karathon.objects.get(is_presentation=True)
        # karathon_is_started = True if request.user.participant.get_participant_time().date() > \
        #                               presentation_karathon.starts_at else False

        context = {
            "presentation_karathon": presentation_karathon,
            # "karathon_is_started": karathon_is_started
        }

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


class KarathonView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET_RATING_LIST":
            return self.add_rating_list(request, *args, **kwargs)
        if request.method == "GET":
            return self.karathon(request, *args, **kwargs)

    def add_rating_list(self, request, *args, **kwargs):
        data = json.loads(request.body)
        karathon_number = kwargs["karathon_number"]
        rating_list_showed = data.pop("amount_list")
        rating_list = Karathon.rating_list(karathon_number)
        next_rating_items_exist = True

        rating_list_to_show = rating_list_showed + 5

        rating_list_block = render_to_string(
            "core/includes/karathon_rating.html",
            {
                "karathon_rating": rating_list[:rating_list_to_show]
            },
            request,
        )

        if rating_list_to_show >= len(rating_list):
            next_rating_items_exist = False

        out = {
            "status": "ok",
            "rating_list_showed": rating_list_showed,
            "rating_list_block": rating_list_block,
            "next_rating_items_exist": next_rating_items_exist
        }

        return JsonResponse(out)


    def karathon(self, request, *args, **kwargs):
        karathon_number = kwargs["karathon_number"]
        karathon = Karathon.objects.get(number=karathon_number)

        karathon_is_started = True if datetime.datetime.now().date() > karathon.starts_at \
            else False

        context = {
            "karathon": karathon,
            "karathon_is_started": karathon_is_started,
            "karathon_rating": Karathon.rating_list(karathon_number)[:5],
            "request_url": self.request.path,
        }

        return render(request, "core/karathon.html", context)


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
        participantskarathon__participant=request.user.participant
    )
    free_karathon_list = karathon_list.exclude(
        participantskarathon__participant=request.user.participant
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
