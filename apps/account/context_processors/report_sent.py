def report_sent(request):
    if request.user.is_authenticated:
        report_sent = request.user.participant.is_today_report()
        return {"report_sent": report_sent}
    return {"report_sent": False}