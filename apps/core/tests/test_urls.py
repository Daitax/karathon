from http import HTTPStatus

from django.test import TestCase, Client

from apps.account.models import Participant
from apps.core.models import Karathon


class StaticURLTests(TestCase):
    def setUp(self):
        self.unauthorized_user = Client()
        
    def test_unexisting_page(self):
        response = self.unauthorized_user.get("/unexisting_page/")

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, "core/404.html")
    
class CoreURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_participant = Participant.objects.create()
        cls.karathon = Karathon.objects.create(
            number=1,
            starts_at="2023-03-02",
            finished_at="2023-03-12",
            type="individual"
        )
    
    def setUp(self):
        self.unauthorized_user = Client()
    
    def test_unauthorized_user(self):
        """Pages in a list are available for an unauthorized user."""
        urls = [
            "/",
            "/karathons/",
            f"/karathons/{self.karathon.id}-karathon/",
        ]
        
        for adress in urls:
            with self.subTest(adress=adress):
                response = self.unauthorized_user.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)