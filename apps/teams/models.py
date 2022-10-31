from django.db import models

# Create your models here.
from apps.account.models import Participant
from apps.core.models import Karathon


class Team(models.Model):
    name = models.CharField('Название команды', max_length=20)
    karathon = models.ForeignKey(Karathon, verbose_name='Карафон', on_delete=models.CASCADE)
    # participants = models.ManyToManyField(Participant, verbose_name='Участник', related_name='team')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name


class TeamParticipant(models.Model):
    team = models.ForeignKey(Team, verbose_name='Команда', on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, verbose_name='Участник', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Участник команды'
        verbose_name_plural = 'Участники команды'

    def __str__(self):
        return "Участник команды"


class DesiredTeam(models.Model):
    desirer = models.ForeignKey(Participant, related_name='desirer', on_delete=models.CASCADE)
    desired_participant = models.ForeignKey(Participant, related_name='desired_participant', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Желаемый сокомандник'
        verbose_name_plural = 'Желаемые сокомандники'

