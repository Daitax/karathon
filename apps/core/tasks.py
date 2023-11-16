import datetime

from apps.notifications.models import Notification
from project.celery import app

@app.task
def ended_karathon():
    from apps.core.models import Karathon
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    today = datetime.datetime.now()

    karathons = Karathon.objects.filter(finished_at__gte=yesterday, finished_at__lte=today)

    for karathon in karathons:
        if karathon.is_ended_karathon():
            from apps.account.models import Winner
            if karathon.type == 'individual':
                winner = Winner.set_individual_karathon_winner(karathon)
                Notification.finished_individual_karathon(karathon, winner)
                Notification.winner_individual_karathon(karathon, winner)
            elif karathon.type == 'team':
                Winner.set_team_karathon_winners(karathon)



