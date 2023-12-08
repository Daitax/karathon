from django import template

from apps.steps.models import Step

register = template.Library()


@register.inclusion_tag("core/includes/first_champs.html", takes_context=True)
def first_champs(context):
    champ_list = Step.get_champs_list()
    top_champs = champ_list[:3]

    return {
        "top_champs": top_champs,
        "view_name": context.request.resolver_match.view_name,
    }
