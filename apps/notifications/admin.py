from django import forms
from django.contrib import admin

from apps.notifications.models import Notification, NotificationTemplate


class NotificationTemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(NotificationTemplate, NotificationTemplateAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("participant", "is_viewed")
    list_editable = ("is_viewed",)


admin.site.register(Notification, NotificationAdmin)
