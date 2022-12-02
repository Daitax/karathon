from django import template

register = template.Library()


@register.inclusion_tag('core/widgets/task_today.html', takes_context=True)
def task_today(context):
    if context.request.user.is_authenticated:
        active_karathon = context.request.user.participant.get_active_karathon()
        task = context.request.user.participant.today_task()
        return {
            'user': 'context.request.user',
            'active_karathon': active_karathon,
            'task': task,
        }
    else:
        return {
            'user': 'context.request.user'
        }
