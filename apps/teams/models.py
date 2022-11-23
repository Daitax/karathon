from django.contrib import admin
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models

# Create your models here.
from apps.account.models import Participant
from apps.core.models import Karathon


class Team(models.Model):
    name = models.CharField('Название команды', max_length=20)
    karathon = models.ForeignKey(Karathon, verbose_name='Карафон', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name

    def team_steps(self):
        pass


class TeamParticipant(models.Model):
    team = models.ForeignKey(Team, verbose_name='Команда', on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, verbose_name='Участник', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Участник команды'
        verbose_name_plural = 'Участники команды'

    def __str__(self):
        return "Участник команды"

    def clean(self):
        karathon_teams_participant = Team.objects.filter(karathon=self.team.karathon,
                                                         teamparticipant__participant=self.participant).exclude(
                                                            id=self.team.id)
        if karathon_teams_participant.count() > 0:
            raise ValidationError({'participant': 'Данный участник уже участвует в другой команде'})


class DesiredTeam(models.Model):
    desirer = models.ForeignKey(Participant, related_name='desirer', on_delete=models.CASCADE)
    desired_participant = models.ForeignKey(Participant, related_name='desired_participant', on_delete=models.CASCADE)


'''
queryset, manager и модель специально для вывода в админке списка людей с кем он хочет участвовать в отдельной ячейке
'''


class PrintDesiredTeamQuerySet(models.QuerySet):
    def desirers_list(self):
        return self.filter(desirer__isnull=False).distinct()


class PrintDesiredTeamManager(models.Manager):
    def get_queryset(self):
        qs = PrintDesiredTeamQuerySet(model=Participant)
        return qs


class PrintDesiredTeam(models.Model):
    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Желаемые сокомандники'

    desired_team_manager = PrintDesiredTeamManager()

    @admin.display(description="Желаемая команда")
    def desirer_team(self):
        pass
        # return DesiredTeam.desired_team_manager.get_queryset().team_list(self)
