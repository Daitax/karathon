def report_sent(request):
    if request.user.is_authenticated:
        report_sent = request.user.participant.is_today_report()
        return {"report_sent": report_sent}
    else:
        return {"report_sent": False}


def active_karathon(request):
    if request.user.is_authenticated:
        active_karathon = request.user.participant.get_active_karathon()
        return {"active_karathon": active_karathon}
    else:
        return {"active_karathon": False}
