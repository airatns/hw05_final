from django.core.cache import cache
from django.test import Client, TestCase
from faker import Faker

from ..models import Group, Post, User

fake = Faker()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user('author')
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user)
        cls.group = Group.objects.create(
            title=fake.text(max_nb_chars=15),
            slug=fake.slug(),
            description=fake.text(max_nb_chars=25),
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=fake.text(max_nb_chars=200),
        )
        cls.post_id = cls.post.id

    def test_url_uses_correct_template(self):
        """Страница использует корректный шаблон"""
        cache.clear()
        templates_dict = {
            '': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user}/': 'posts/profile.html',
            f'/posts/{self.post_id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post_id}/edit/': 'posts/create_post.html',
        }
        for address, template in templates_dict.items():
            with self.subTest(address=address):
                response = self.authorized_user.get(address)
                self.assertTemplateUsed(response, template)

    def test_create_edit_list_url_redirect_guest_client_on_admin_login(self):
        """Страницы по адресу /create/ и /edit/ перенаправят анонимного
        пользователя на страницу логина
        """
        templates_dict = {
            '/create/': '/auth/login/?next=/create/',
            f'/posts/{self.post_id}/edit/':
                f'/auth/login/?next=/posts/{self.post_id}/edit/',
        }
        for address, template in templates_dict.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                self.assertRedirects(response, template)
