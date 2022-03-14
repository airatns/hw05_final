from django.test import Client, TestCase

from posts.models import User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_404_url_uses_correct_template(self):
        """Страница использует корректный шаблон"""
        templates_dict = {
            '/candy/': 'core/404.html',
        }
        for address, template in templates_dict.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
