from http import HTTPStatus

from django.test import Client, TestCase
from faker import Faker

from ..models import Group, Post, User

fake = Faker()

OK = HTTPStatus.OK
FOUND = HTTPStatus.FOUND
NOT_FOUND = HTTPStatus.NOT_FOUND


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user('author')
        cls.group = Group.objects.create(
            title=fake.text(max_nb_chars=15),
            slug=fake.slug(),
            description=fake.text(max_nb_chars=25),
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=fake.text(max_nb_chars=200),
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='author')
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)
        self.post_id = self.post.id

    def test_url_exists_at_desired_location(self):
        """Страница доступна пользователю"""
        response_dict = {
            self.guest_client.get(''): OK,
            self.guest_client.get(f'/group/{self.group.slug}/'): OK,
            self.guest_client.get(f'/profile/{self.user}/'): OK,
            self.guest_client.get(f'/posts/{self.post_id}/'): OK,
            self.authorized_user.get(f'/posts/{self.post_id}/edit/'): OK,
            self.guest_client.get(f'/posts/{self.post_id}/edit/'): FOUND,
            self.authorized_user.get('/create/'): OK,
            self.guest_client.get('/create/'): FOUND,
            self.guest_client.get('/unexisting_page/'): NOT_FOUND,
        }
        for response, status_code in response_dict.items():
            with self.subTest(response=response):
                self.assertEqual(response.status_code, status_code)
