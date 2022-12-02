# from apps.notifications.models import Notification

# def not_viewed_notifications(request):
#     not_viewed_notifications_amount = Notification(participant=request.user.participant).not_viewed_amount()
#     if not_viewed_notifications_amount != 0:
#         return {"not_viewed_notifications_amount": not_viewed_notifications_amount}
#     else:
#         return {"not_viewed_notifications_amount": ""}