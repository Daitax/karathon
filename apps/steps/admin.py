from django.contrib import admin

# Register your models here.
from apps.steps.models import Step


class StepAdmin(admin.ModelAdmin):
    list_display = ('participant', 'date', 'steps', 'photo_preview_in_list', 'is_completed', 'bonus')

    fields = ('participant', 'date', 'steps', 'photo_preview', 'is_completed', 'bonus')
    readonly_fields = ('participant', 'date', 'photo_preview',)
    search_fields = ('participant__first_name', 'participant__last_name',)
    search_help_text = 'Для поиска введите имя или фамилию участника'


admin.site.register(Step, StepAdmin)
