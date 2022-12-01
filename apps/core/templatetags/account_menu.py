from django import template

register = template.Library()


@register.inclusion_tag('core/menu/account_menu.html', takes_context=True)
def account_menu(context):
    if context.request.user.is_authenticated:
        localtime = context.request.user.participant.get_participant_time()

        return {
            'user': context.request.user,
            'localtime': localtime,
            'view_name': context.request.resolver_match.view_name,
        }
    else:
        return {
            'user': context.request.user,
        }