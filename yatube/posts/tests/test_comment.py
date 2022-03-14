from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker
from posts.forms import CommentForm

from ..models import Comment, Group, Post, User

fake = Faker()

ONE_NEW_POST = 1


class CommentFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user('barrakuda')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title=fake.text(max_nb_chars=15),
            slug=fake.slug(),
            description=fake.text(max_nb_chars=25),
        )
        cls.post = Post.objects.create(
            text=fake.text(),
            group=cls.group,
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            text=fake.text(),
            author=cls.user,
            post=cls.post,
        )
        cls.form = CommentForm()
        cls.post_id = cls.post.id

    def test_comment_form(self):
        """Валидная форма создает запись в Comment."""
        comment_count = Comment.objects.count()
        form_data = {
            'text': fake.text,
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post_id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post_id}))
        self.assertEqual(Comment.objects.count(), comment_count + ONE_NEW_POST)
        self.assertTrue(Comment.objects.filter(text=fake.text,).exists())
