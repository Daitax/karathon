from django.contrib import admin

# Register your models here.
from apps.steps.models import Step


class StepAdmin(admin.ModelAdmin):
    list_display = ('participant', 'date', 'steps', 'photo',)

admin.site.register(Step, StepAdmin)