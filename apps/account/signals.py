from apps.notifications.tasks import send_notification_add_instagram, send_notification_add_email


def send_new_participant_notifications(sender, instance, created, **kwargs):
    if created:
        send_notification_add_instagram(instance)
        send_notification_add_email(instance)
