from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase
from faker import Faker

from ..models import Follow, Post, User

fake = Faker()

OK = HTTPStatus.OK
FOUND = HTTPStatus.FOUND
NOT_FOUND = HTTPStatus.NOT_FOUND


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user('author')
        cls.post = Post.objects.create(
            author=cls.author,
            text=fake.text(max_nb_chars=200),
            pub_date=fake.date(),
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='advisor')
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)
        self.follow = Follow.objects.create(
            author=self.author,
            user=self.user,
        )

    def test_url_exists_at_desired_location(self):
        """Страницы подписки и отписки доступны
        авторизованному пользователю.
        """
        response_dict = {
            self.authorized_user.get(
                f'/profile/{self.post.author}/follow/'): FOUND,
            self.authorized_user.get(
                f'/profile/{self.post.author}/unfollow/'): FOUND,
        }
        for response, status_code in response_dict.items():
            with self.subTest(response=response):
                self.assertEqual(response.status_code, status_code)

    def test_follows_unfollow_url_uses_correct_template(self):
        """Страницы follow и unfollow перенаправят авторизованного
        пользователя на страницу Избранных авторов.
        """
        cache.clear()
        templates_dict = {
            f'/profile/{self.post.author}/follow/': '/follow/',
            f'/profile/{self.post.author}/unfollow/': '/follow/',
        }
        for address, template in templates_dict.items():
            with self.subTest(address=address):
                response = self.authorized_user.get(address)
                self.assertRedirects(response, template)
