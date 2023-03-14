from django import template
from apps.notifications.models import Notification

register = template.Library()


@register.inclusion_tag('core/menu/account_menu.html', takes_context=True)
def account_menu(context):
    if context.request.user.is_authenticated:
        user = context.request.user.participant
        return {
            'user': user,
            'localtime': user.get_participant_time(),
            'view_name': context.request.resolver_match.view_name,
            'is_today_report': user.is_today_report(),
            'not_viewed_notifications_amount': Notification(participant=user).not_viewed_amount(),
        }
    else:
        return {
            'user': context.request.user,
        }