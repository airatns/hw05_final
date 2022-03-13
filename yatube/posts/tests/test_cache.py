from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from ..models import Post

fake = Faker()
User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='author')
        cls.post = Post.objects.create(
            author=cls.user,
            text=fake.text(max_nb_chars=200),
        )
        cls.post_id = cls.post.id

    def test_index_page_cache(self):
        """Проверка работы кеша Главглй страницы"""
        response_1 = self.guest_client.get(reverse('posts:index'))
        resp_1 = response_1.content
        post_to_delete = self.post
        post_to_delete.delete()
        response_2 = self.guest_client.get(reverse('posts:index'))
        resp_2 = response_2.content
        self.assertTrue(resp_1 == resp_2)
