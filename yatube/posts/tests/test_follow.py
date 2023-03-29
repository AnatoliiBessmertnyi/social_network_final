from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class FollowViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='username')
        cls.user = User.objects.create_user(username='auth')
        cls.follow = Follow.objects.create(
            author=cls.author,
            user=cls.user
        )
        cls.group_1 = Group.objects.create(
            title='Тестовая группа 1',
            slug='Тестовый слаг 1',
            description='Тестовое описание 1'
        )
        cls.group_2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='Тестовый слаг 2',
            description='Тестовое описание 2'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый пост',
            group=cls.group_1,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            text='Тестовый комментарий',
            author=cls.author
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_follow_another_user(self):
        """Авторизованный пользователь может подписываться на
        других пользователей."""
        follow_count = Follow.objects.count()
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.user}
            )
        )
        self.assertTrue(
            Follow.objects.filter(
                user=self.author,
                author=self.user
            ).exists()
        )
        self.assertEqual(Follow.objects.count(), follow_count + 1)

    def test_unfollow_another_user(self):
        """Авторизованный пользователь может и удалять других пользователей
        из подписок."""
        Follow.objects.create(user=self.author, author=self.user)
        follow_count = Follow.objects.count()
        self.assertTrue(
            Follow.objects.filter(
                user=self.author,
                author=self.user
            ).exists()
        )
        self.authorized_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': self.user}
            )
        )
        self.assertFalse(
            Follow.objects.filter(
                user=self.author,
                author=self.user
            ).exists()
        )
        self.assertEqual(Follow.objects.count(), follow_count - 1)

    def test_new_post_follow(self):
        """Новая запись пользователя появляется в ленте тех, кто на него
        подписан."""
        following = User.objects.create(username='following')
        Follow.objects.create(user=self.author, author=following)
        post = Post.objects.create(author=following, text=self.post.text)
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertIn(post, response.context['page_obj'].object_list)

    def test_new_post_unfollow(self):
        """Новая запись пользователя не появляется в ленте тех, кто на него не
        подписан."""
        self.client.logout()
        User.objects.create_user(
            username='somobody_temp',
            password='pass'
        )
        self.client.login(username='somobody_temp')
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertNotIn(
            self.post.text,
            response.context['page_obj'].object_list
        )
