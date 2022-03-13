from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker

from ..models import Group, Post

fake = Faker()
User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user('auth')
        cls.group = Group.objects.create(
            title=fake.text(max_nb_chars=15),
            slug=fake.slug(),
            description=fake.text(max_nb_chars=25),
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=fake.text(max_nb_chars=200),
        )

    def test_models_have_correct_object_name(self):
        '''Корректно ли отображается значение поля __str__ в моделях'''
        group = self.group
        post = self.post
        vals = (
            (group.title, str(group)),
            (post.text[:15], str(post)),
        )
        for value, expected_value in vals:
            with self.subTest(value=value):
                self.assertEqual(value, expected_value)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым"""
        post = PostModelTest.post
        field_verboses = {
            'text': post._meta.get_field('text').verbose_name,
            'pub_date': post._meta.get_field('pub_date').verbose_name,
            'author': post._meta.get_field('author').verbose_name,
            'group': post._meta.get_field('group').verbose_name,
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым"""
        post = PostModelTest.post
        field_help_texts = {
            'text': post._meta.get_field('text').help_text,
            'group': post._meta.get_field('group').help_text,
        }
        for field, expectes_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expectes_value)
