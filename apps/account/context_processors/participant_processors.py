def active_karathon_participant(request):
    if request.user.is_authenticated:
        active_karathon = request.user.participant.get_active_karathon()
        return {"active_karathon_participant": active_karathon}
    return {"active_karathon_participant": False}


def report_sent(request):
    if request.user.is_authenticated:
        report_sent = request.user.participant.is_today_report()
        return {"report_sent": report_sent}
    return {"report_sent": False}



