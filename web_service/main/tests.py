from django.test import Client, TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from minio.error import S3Error


class UrlTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Настраиваем сессию для writer
        session = self.client.session
        session.update({
            'id': 1,
            'role': 'writer',
            'username': 'test_writer'
        })
        session.save()

        # Настраиваем сессию для moderator
        self.moderator_client = Client()
        moderator_session = self.moderator_client.session
        moderator_session.update({
            'id': 2,
            'role': 'moderator',
            'username': 'test_moderator'
        })
        moderator_session.save()

    def test_home_page(self, mock_minio):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_search_posts(self):
        response = self.client.get(reverse('search_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_posts.html')

    def test_view_post(self):
        response = self.client.get(reverse('view_post', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post.html')

    def test_create_post(self):
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_post.html')

    def test_create_post(self):
        response = self.client.post(reverse('create_post'), {
            'title': 'Test Title',
            'content': 'Test Content'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        response = self.client.post(reverse('delete_post'), {
            'post_id': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Ok')

    def test_update_post(self):
        response = self.client.post(reverse('update_post'), {
            'post_id': 1,
            'title': 'Updated Title',
            'content': 'Updated Content'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Ok')

    def test_create_organization(self):
        response = self.moderator_client.get(reverse('create_organization'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_organization.html')

    def test_delete_organization(self):
        response = self.moderator_client.post(reverse('delete_organization'), {
            'organization_id': 1
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, b'Ok')

    def test_view_organizations(self):
        response = self.client.get(reverse('organizations_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organization.html')
        self.assertIn('organizations', response.context)

    def test_create_writer(self):
        response = self.moderator_client.get(reverse('create_writer'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'create_writer.html')

    def test_create_writer(self):
        response = self.moderator_client.post(reverse('create_writer'), {
            'username': 'new_writer',
            'password': 'newpass123',
            'organization': 'Test Org'
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_writer(self):
        response = self.moderator_client.post(reverse('delete_writer'), {
            'id': 1
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, b'Ok')

    def test_writer_login(self):
        response = self.client.get(reverse('writer_login'))
        self.assertEqual(response.status_code, 200)

    def test_moderator_login(self):
        response = self.client.get(reverse('moderator_login'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_nonexistent(self):
        response = self.client.get('/notvalid_url/')
        self.assertEqual(response.status_code, 404)
