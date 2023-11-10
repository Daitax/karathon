from django import template
from apps.core.utils import ending_numbers
from apps.steps.models import Step

register = template.Library()

@register.inclusion_tag('core/includes/steps_block.html', takes_context=True)
def steps_block(context):
    words = ["шаг", "шага", "шагов"]
    verbs = ["пройден", "пройдено", "пройдено"]
    total_steps = Step.total()['steps__sum']
    if not total_steps:
        total_steps = 0
    last_karathon_steps = Step.total_last_karathon()['steps__sum']
    if not last_karathon_steps:
        last_karathon_steps = 0
    total_steps_today = Step.total_today()['steps__sum']
    if not total_steps_today:
        total_steps_today = 0
    return {
        "total_steps": total_steps,
        "total_steps_word": ending_numbers(total_steps, words),
        "total_steps_verb": ending_numbers(total_steps, verbs),
        "total_steps_last": last_karathon_steps,
        "total_steps_last_word": ending_numbers(last_karathon_steps, words),
        "total_steps_last_verb": ending_numbers(last_karathon_steps, verbs),
        "total_steps_today": total_steps_today,
        "total_steps_today_word": ending_numbers(total_steps_today, words),
        "total_steps_today_verb": ending_numbers(total_steps_today, verbs),
        }