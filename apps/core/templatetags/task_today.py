from django import template

register = template.Library()


@register.inclusion_tag('core/widgets/task_today.html', takes_context=True)
def task_today(context):
    if context.request.user.is_authenticated:
<<<<<<< HEAD

        active_karathon = context.request.user.participant.get_active_karathon()
        task = context.request.user.participant.today_task()
=======
        participant = context.request.user.participant
        active_karathon = participant.get_active_karathon()
        task = participant.today_task()
        text_task = task.text_individual_task(participant) if task else None
>>>>>>> rc

        return {
            'user': context.request.user,
            'active_karathon': active_karathon,
            'task': text_task,
        }

    else:
        return {
            'user': context.request.user
        }
