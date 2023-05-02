from django import template
from django.conf import settings
from django.shortcuts import get_list_or_404

from apps.account.models import Participant

register = template.Library()


@register.inclusion_tag("core/includes/first_champs.html", takes_context=True)
def first_champs(context):
    champs = get_list_or_404(Participant)
    list_ch = []
    i = 0
    for champ in champs:
        # if champ.photo:
        list_ch.append([champ, i + 1])
        i += 1
    # list_ch = [champ for champ in champs if champ.photo]
    # list_ch = [[item, list_ch.index(item) + 1] for item in list_ch]
    return {
        "champs": list_ch[: settings.CHAMPIONS_ON_CHAMPS_BLOCK],
        "view_name": context.request.resolver_match.view_name,
    }
