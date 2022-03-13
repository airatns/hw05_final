from http import HTTPStatus

from django.test import Client, TestCase

OK = HTTPStatus.OK


class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        response_dict = {
            self.guest_client.get('/about/author/'): OK,
            self.guest_client.get('/about/tech/'): OK,
        }
        for response, status_code in response_dict.items():
            with self.subTest(response=response):
                self.assertEqual(response.status_code, status_code)
