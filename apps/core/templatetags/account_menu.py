from django import template

register = template.Library()


@register.inclusion_tag('core/index.html', takes_context=True)
def account_menu(context):
    if context.request.user.is_authenticated:
        localtim = context.request.user.participant.get_participant_time()
        is_today_report = context.request.user.participant.is_today_report()

        return {
            'request_url': context.request.path,
            'user': context.request.user,
            'localtime': localtim,
            'is_today_report': is_today_report,
            'val': 'ok',
        }
    else:
        return {
            'request_url': context.request.path,
            'user': context.request.user,
        }