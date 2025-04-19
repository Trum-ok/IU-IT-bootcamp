from django.test import Client, TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from minio.error import S3Error
import uuid

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.session = {'id': 1, 'role': 'moderator'}
        self.client.session.update(self.session)


    def test_search_posts(self):
        response = self.client.get('posts/search/')
        self.assertEqual(response.status_code, 200)

    def test_view_post(self):
        response = self.client.get(reverse('view_post', args=[1]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('view_post', args=[1]))
        self.assertEqual(response.status_code, 200)

    @patch('main.views.Minio')
    def test_delete_organization(self, mock_minio):
        response = self.client.post('organizations/delete/', {
            'organization_id': 1
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_organizations(self):
        response = self.client.get('organizations/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")

    def test_create_writer(self):
        response = self.client.get('writer/create/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('writer/create/', {
            'username': 'testwriter',
            'password': 'testpass',
            'organization': 'Test Org'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_writer(self):
        response = self.client.post('writer/delete/', {
            'id': 1
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        response = self.client.post('posts/update/<str:post_id>/', {
            'post_id': 1,
            'title': 'Updated Title',
            'content': 'Updated Content'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
