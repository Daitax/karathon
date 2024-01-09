import datetime

from django.contrib import admin

# Register your models here.
from apps.tasks.forms import TaskAdminForm
from apps.tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "karathon":
            from apps.core.models import Karathon
            kwargs["queryset"] = Karathon.objects.filter(finished_at__gte=datetime.datetime.now())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Task, TaskAdmin)
