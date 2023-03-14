from django.test import Client, TestCase
from django.urls import reverse

from apps.account.models import Participant
from apps.teams.models import DesiredTeam
from apps.teams import views

class TeamsViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_participant = Participant.objects.create(
            username="user_participant",
            phone="1"
        )
        cls.another_user_participant = Participant.objects.create(
            username="another_user_participant",
            phone="2"
        )
    
    def setUp(self):
        self.unauthorized_user = Client()
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user_participant)
        
    def test_desired_participant_appearance(self):
        """Desired participant appears in a team page."""
        added_participant = DesiredTeam.objects.create(
            desirer = self.user_participant,
            desired_participant = self.another_user_participant
        )
        response = self.authorized_user.get("/account/team/")
        self.assertIn(added_participant, response.context.get("desire_list"))
        
    def test_remove_desired_participant(self):
        """Desired participant doesn't appear in a team page after remove."""
        added_participant = DesiredTeam.objects.create(
            desirer = self.user_participant,
            desired_participant = self.another_user_participant
        )
        DesiredTeam.objects.filter(
            desirer = self.user_participant,
            desired_participant = self.another_user_participant
        ).delete()
        response = self.authorized_user.get("/account/team/")
        self.assertNotIn(added_participant, response.context.get("desire_list"))
        