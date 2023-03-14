from http import HTTPStatus

from django.test import TestCase, Client

from apps.account.models import Participant


class AccountURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_participant = Participant.objects.create()
    
    def setUp(self):
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user_participant)
        
    def test_authorized_user_redirects_to_index_after_logout(self):
        """Authorized user redericts to index page after logout."""
        response = self.authorized_user.get("/account/messages")
        self.assertEqual(response.status_code, 301)
    
    def test_authorized_user(self):
        """Pages in a list are available for an authorized user."""
        urls = [
            "/account/",
            "/account/messages/",
            "/account/results/",
            "/account/team/",
            ]
        for adress in urls:
            with self.subTest(adress=adress):
                response = self.authorized_user.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)