from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from ..models import Group, Post

fake = Faker()
User = get_user_model()
POSTS_QUANTITY = 13
POSTS_PER_PAGE = 10
LAST_PAGE_POSTS = 3


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user('noname')
        cls.group = Group.objects.create(
            title=fake.text(max_nb_chars=15),
            slug=fake.slug(),
            description=fake.text(max_nb_chars=25),
        )
        Post.objects.bulk_create([
            Post(
                pub_date=fake.date(),
                text=fake.text(max_nb_chars=200),
                author=cls.user,
                group=cls.group)
        ] * 13)

    def setUp(self):
        self.guest_user = Client()

    def test_index_first_page_contains_ten_records(self):
        cache.clear()
        response = self.guest_user.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), POSTS_PER_PAGE)

    def test_index_last_page_contains_three_rescords(self):
        response = self.guest_user.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), LAST_PAGE_POSTS)

    def test_group_list_first_page_contains_ten_records(self):
        response = self.guest_user.get(reverse(
            'posts:group_list', kwargs={'slug': self.group.slug}))
        self.assertEqual(len(response.context['page_obj']), POSTS_PER_PAGE)

    def test_group_list_last_page_contains_three_rescords(self):
        response = self.guest_user.get(reverse(
            'posts:group_list', kwargs={'slug': self.group.slug}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), LAST_PAGE_POSTS)

    def test_profile_first_page_contains_ten_records(self):
        response = self.guest_user.get(reverse(
            'posts:profile', kwargs={'username': self.user}))
        self.assertEqual(len(response.context['page_obj']), POSTS_PER_PAGE)

    def test_profile_last_page_contains_three_rescords(self):
        response = self.guest_user.get(reverse(
            'posts:profile', kwargs={'username': self.user}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), LAST_PAGE_POSTS)
