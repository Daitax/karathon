from django import template
from apps.account.models import Participant
from django.shortcuts import get_list_or_404

register = template.Library()


@register.inclusion_tag(
    "core/includes/first_three_champs.html", takes_context=True
)
def first_three_champs(context):
    champs = get_list_or_404(Participant)
    list_ch = []
    i = 0
    for champ in champs:
        if champ.photo:
            list_ch.append([champ, i + 1])
            i += 1
    # list_ch = [champ for champ in champs if champ.photo]
    # list_ch = [[item, list_ch.index(item) + 1] for item in list_ch]
    return {
        "champs": list_ch[:5],
    }
