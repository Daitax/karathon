from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from apps.account.models import Participant
from apps.teams.models import Team, TeamParticipant, PrintDesiredTeam


class TeamParticipantTabular(admin.TabularInline):
    model = TeamParticipant
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        team_id = request.resolver_match.kwargs.get('object_id')
        try:
            team = Team.objects.get(id=team_id)
            kwargs['queryset'] = Participant.objects.filter(karathon=team.karathon)
        except ObjectDoesNotExist:
            kwargs['queryset'] = Participant.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TeamAdmin(admin.ModelAdmin):
    inlines = [
        TeamParticipantTabular,
    ]


class ParticipantTeamAdmin(admin.ModelAdmin):
    pass


class PrintDesiredTeamAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'desirer_team']
    list_display_links = None
    search_fields = ['first_name', 'last_name', 'phone']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.desirers_list()


admin.site.register(Team, TeamAdmin)
admin.site.register(PrintDesiredTeam, PrintDesiredTeamAdmin)
