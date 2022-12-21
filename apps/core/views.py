import datetime

import pytz
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from apps.core.models import Karathon


def index(request):
    return render(request, 'core/index.html', {'user': request.user})


def about_karathons(request):
    return render(request, 'core/about_karathons.html')


def karathon(request, **kwargs):
    karathon_number = kwargs['karathon_number']

    karathon = Karathon.objects.get(number=karathon_number)

    context = {
        'karathon': karathon
    }
    return render(request, 'core/karathon.html', context)


@login_required
def participate(request):
    if request.method == "POST":
        karathon_id = request.POST['karathon']
        request.user.participant.karathon.add(karathon_id)

    participant_date = request.user.participant.get_participant_time()

    karathon_list = Karathon.objects.filter(starts_at__gte=participant_date)

    participant_karathon_list = karathon_list.filter(participant=request.user.participant)
    free_karathon_list = karathon_list.exclude(participant=request.user.participant)
    intersecting_carathons_ids = []

    for participant_karathon_item in participant_karathon_list:
        for free_karathon_item in free_karathon_list:
            latest_start = max(free_karathon_item.starts_at, participant_karathon_item.starts_at)
            earliest_end = min(free_karathon_item.finished_at, participant_karathon_item.finished_at)

            if latest_start <= earliest_end:
                intersecting_carathons_ids.append(free_karathon_item.id)

    available_karathon_list = free_karathon_list.exclude(id__in=intersecting_carathons_ids)

    context = {
        'participant_karathon_list': participant_karathon_list,
        'available_karathon_list': available_karathon_list
    }

    return render(request, 'core/participate.html', context)
