import datetime

from django import template

from apps.core.models import Karathon

register = template.Library()


@register.inclusion_tag('core/menu/navbar.html', takes_context=True)
def navbar(context):
    if context.request.user.is_authenticated:
        current_datetime = context.request.user.participant.get_participant_time()
    else:
        current_datetime = datetime.datetime.now()

    not_finished_karathons = Karathon.not_finished_karathons()


    started_karathons = not_finished_karathons.filter(starts_at__lte=current_datetime)

    if started_karathons.count() > 0:
        output_karathons = started_karathons
    else:
        output_karathons = not_finished_karathons.order_by('starts_at')[:2]

    return {
        'request_url': context.request.path,
        'user': context.request.user,
        'karathons': output_karathons,
    }
