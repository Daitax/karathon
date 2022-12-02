def report_sent(request):
    report_sent = request.user.participant.is_today_report()
    return {"report_sent": report_sent}