from django import template
from apps.notifications.models import Notification

register = template.Library()


@register.inclusion_tag('core/menu/account_menu.html', takes_context=True)
def account_menu(context):
    if context.request.user.is_authenticated:
        localtime = context.request.user.participant.get_participant_time()
        is_today_report = context.request.user.participant.is_today_report()
        not_viewed_notifications_amount = Notification(participant=context.request.user.participant).not_viewed_amount()
        if not_viewed_notifications_amount == 0:
            not_viewed_notifications_amount = ""
        return {
            'user': context.request.user,
            'localtime': localtime,
            'view_name': context.request.resolver_match.view_name,
            'is_today_report': is_today_report,
            'not_viewed_notifications_amount': not_viewed_notifications_amount,
        }
    else:
        return {
            'user': context.request.user,
        }