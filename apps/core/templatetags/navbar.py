from django import template

register = template.Library()


@register.inclusion_tag('core/menu/navbar.html', takes_context=True)
def navbar(context):
    if context.request.user.is_authenticated:
        return {
            'request_url': context.request.path,
            'user': context.request.user,
        }
    else:
        return {
            'request_url': context.request.path,
            'user': context.request.user,
        }
