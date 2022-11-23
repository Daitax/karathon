from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.account.models import Participant, User


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'middle_name', 'phone',)

    fieldsets = (
        ('Персональная информация', {'fields': ('username', 'first_name', 'last_name', 'middle_name', 'phone',
                                                   'instagram',
                                                   'timezone', 'category')}),
    )


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(User, UserAdmin)
