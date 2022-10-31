from django import forms
from django.contrib import admin

# Register your models here.

from apps.notifications.models import NotificationTemplate


class NotificationTemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(NotificationTemplate, NotificationTemplateAdmin)
