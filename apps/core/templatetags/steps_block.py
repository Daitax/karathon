from django import template
from apps.steps.models import Step

register = template.Library()

@register.inclusion_tag('core/includes/steps_block.html', takes_context=True)
def steps_block(context):
    steps = Step().total()
    total_steps = [value for value in steps.values()][0]
    if not total_steps:
        total_steps = 0
    steps_today = Step().total_today()
    total_steps_today = [value for value in steps_today.values()][0]
    if not total_steps_today:
        total_steps_today = 0
    return {
        "total_steps": '{0:,}'.format(total_steps).replace(',', ' '),
        "total_steps_word": Step().plural_name(total_steps),
        "total_steps_today": '{0:,}'.format(total_steps_today).replace(',', ' '),
        "total_steps_today_word": Step().plural_name(total_steps_today),
        }