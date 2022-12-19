from apps.core.models import Karathon


def active_karathon_participant(request):
    if request.user.is_authenticated:
        active_karathon = request.user.participant.get_active_karathon()
        return {"active_karathon": active_karathon}
    return {"active_karathon": False}


def active_karathons(request):
    # if request.user.is_authenticated:
        datetime = request.user.participant.get_participant_time()
        output_karathons = []
        karathons = Karathon.not_finished_karathons()

        started_karathons = karathons.filter(starts_at__lte=datetime)
        if started_karathons.count() == 0:
            output_karathons = karathons.order('starts_at').first()
        else:
            output_karathons = started_karathons
    # if request.user.is_authenticated:
    #     datetime = request.user.participant.get_participant_time()
    #
    # else:
    #     import datetime
    #     datetime = datetime.datetime.now()
    #
    # print(Karathon.active_karathons())
        return {"karathons": output_karathons,}


def report_sent(request):
    if request.user.is_authenticated:
        report_sent = request.user.participant.is_today_report()
        return {"report_sent": report_sent}
    return {"report_sent": False}



