from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from ..models import Group, Post

fake = Faker()
User = get_user_model()


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user('author')
        cls.group = Group.objects.create(
            title=fake.text(max_nb_chars=15),
            slug=fake.slug(),
            description=fake.text(max_nb_chars=25),
        )
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            pub_date=fake.date(),
            text=fake.text(max_nb_chars=200),
            author=cls.user,
            group=cls.group,
            image=cls.uploaded,
        )

    def setUp(self):
        self.guest_user = Client()
        self.user = User.objects.get(username='author')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post_id = self.post.id

    def test_pages_uses_correct_template(self):
        """URL-адреса используют корректные шаблоны"""
        cache.clear()
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post_id}):
                'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post_id}):
                'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом"""
        cache.clear()
        response = self.guest_user.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        context_dict = {
            first_object.text: self.post.text,
            first_object.author: self.post.author,
            first_object.group.title: self.group.title,
            first_object.pub_date: self.post.pub_date,
            first_object.image: self.post.image,
        }
        for context, expected in context_dict.items():
            with self.subTest(context=context):
                self.assertEqual(context, expected)

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом"""
        response = self.guest_user.get(reverse(
            'posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_object = response.context['page_obj'][0]
        context_dict = {
            response.context.get('group').title: self.group.title,
            response.context.get('group').description: self.group.description,
            first_object.text: self.post.text,
            first_object.author: self.post.author,
            first_object.pub_date: self.post.pub_date,
            first_object.image: self.post.image,
        }
        for context, expected in context_dict.items():
            with self.subTest(context=context):
                self.assertEqual(context, expected)

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом"""
        response = self.guest_user.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        first_object = response.context['page_obj'][0]
        context_dict = {
            first_object.text: self.post.text,
            first_object.author: self.post.author,
            first_object.pub_date: self.post.pub_date,
            first_object.group: self.group,
            first_object.image: self.post.image,
            response.context.get('total_posts'):
                Post.objects.all().filter(author=self.user).count(),
        }
        for context, expected in context_dict.items():
            with self.subTest(context=context):
                self.assertEqual(context, expected)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом"""
        response = self.guest_user.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post_id})
        )
        context_dict = {
            response.context.get('post').text: self.post.text,
            response.context.get('post').image: self.post.image,
            response.context.get('total_posts'):
                Post.objects.all().filter(author=self.user).count(),
        }
        for context, expected in context_dict.items():
            with self.subTest(context=context):
                self.assertEqual(context, expected)

    def test_create_post_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_show_correct_context(self):
        """Шаблон create_post/edit сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post_id})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_post_redirect_guest_client_on_admin_login(self):
        """Шаблон create_post перенаправят анонимного пользователя
        на страницу логина.
        """
        response = self.guest_user.get(reverse('posts:post_create'))
        expected = '/auth/login/?next=/create/'
        self.assertRedirects(response, expected)

    def test_edit_post_redirect_guest_client_on_admin_login(self):
        """Шаблон edit_post перенаправят анонимного пользователя
        на страницу логина.
        """
        response = self.guest_user.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post_id})
        )
        expected = f'/auth/login/?next=/posts/{self.post_id}/edit/'
        self.assertRedirects(response, expected)
