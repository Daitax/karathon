# from django import template

# register = template.Library()


# @register.inclusion_tag('account/includes/first_screen.html', takes_context=True)
# def first_screen(context):
#     if context.request.user.is_authenticated:
#         localtime = context.request.user.participant.get_participant_time()

#         return {
#             'request_url': context.request.path,
#             'user': context.request.user,
#             'localtime': localtime,
#         }
#     else:
#         return {
#             'request_url': context.request.path,
#             'user': context.request.user,
#         }