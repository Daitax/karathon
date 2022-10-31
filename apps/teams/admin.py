from django.contrib import admin
from apps.teams.models import Team, TeamParticipant


class TeamParticipantTabular(admin.TabularInline):
    model = TeamParticipant
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    inlines = [
        TeamParticipantTabular,
    ]


admin.site.register(Team, TeamAdmin)
