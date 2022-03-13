from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

OK = HTTPStatus.OK

User = get_user_model()


class TaskURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user('noname')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_user_url_exists_at_desired_location(self):
        response_dict = {
            self.guest_client.get('/auth/signup/'): OK,
        }
        for response, status_code in response_dict.items():
            with self.subTest(response=response):
                self.assertEqual(response.status_code, status_code)

    def test_authorized_user_url_exists_at_desired_location(self):
        response_dict = {
            self.authorized_client.get('/auth/password_change/'): OK,
        }
        for response, status_code in response_dict.items():
            with self.subTest(response=response):
                self.assertEqual(response.status_code, status_code)
