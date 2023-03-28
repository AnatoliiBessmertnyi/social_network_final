from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from posts.models import Post, User


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='cache')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.author,
        )

    def test_pages_uses_correct_template(self):
        """Кэширование данных на странице index"""
        response = self.client.get(reverse('posts:index'))
        cached_response_content = response.content
        Post.objects.create(
            text='Второй тестовый пост',
            author=self.author,
        )
        self.assertEqual(cached_response_content, response.content)
        cache.clear()
        self.assertNotEqual(cached_response_content, response.content)
