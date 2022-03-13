from django.test import Client, TestCase


class TaskURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_user_url_uses_correct_template(self):
        template_dict = {
            'users/signup.html': '/auth/signup/',
        }
        for template, address in template_dict.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
