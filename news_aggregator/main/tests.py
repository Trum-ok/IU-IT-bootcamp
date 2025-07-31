from django.test import Client, TestCase
from django.urls import reverse


class UrlTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_create_organization_page(self):
        response = self.client.get(reverse("create_organization"))
        self.assertEqual(response.status_code, 302)

    def test_organizations_list_page(self):
        response = self.client.get(reverse("organizations_list"))
        self.assertEqual(response.status_code, 200)

    def test_create_writer_page(self):
        response = self.client.get(reverse("create_writer"))
        self.assertEqual(response.status_code, 302)

    def test_writer_login_page(self):
        response = self.client.get(reverse("writer_login"))
        self.assertEqual(response.status_code, 200)

    def test_moderator_login_page(self):
        response = self.client.get(reverse("moderator_login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        self.client.login(username="test", password="qwerty")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_nonexistent_page(self):
        response = self.client.get("/notvalid_url/")
        self.assertEqual(response.status_code, 404)
