from django import template

register = template.Library()


@register.inclusion_tag('core/menu/navbar.html', takes_context=True)
def navbar(context):
    if context.request.user.is_authenticated:
        localtime = context.request.user.participant.get_participant_time()
        is_today_report = context.request.user.participant.is_today_report()

        return {
            'request_url': context.request.path,
            'user': context.request.user,
            # 'localtime': localtime,
            # 'is_today_report': is_today_report,
        }
    else:
        return {
            'request_url': context.request.path,
            'user': context.request.user,
        }
