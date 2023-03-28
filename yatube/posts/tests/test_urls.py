from http import HTTPStatus
from django.urls import reverse
from django.test import Client, TestCase
from ..models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='HasNoName')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.author,
        )

    def setUp(self):
        self.guest_client = Client()  # Создаем неавторизованный клиент
        self.authorized_client = Client()  # Создаем второй клиент
        self.authorized_client.force_login(PostURLTests.author)

    def test_guest_urls_status_code(self):
        """Проверяем доступность страниц для неавторизованного пользователя."""
        fields_response_urls_code = {
            reverse('posts:index'): HTTPStatus.OK,
            reverse('posts:group_list', args={self.group.slug}): HTTPStatus.OK,
            reverse('posts:post_create'): HTTPStatus.FOUND,
            reverse(
                'posts:profile', args={self.author.username}
            ): HTTPStatus.OK,
            reverse('posts:post_detail', args={self.post.id}): HTTPStatus.OK,
            reverse('posts:post_edit', args={self.post.id}): HTTPStatus.FOUND,
        }
        for adress, response_code in fields_response_urls_code.items():
            with self.subTest(adress=adress):
                status_code = self.guest_client.get(adress).status_code
                self.assertEqual(status_code, response_code)

    def test_authorized_urls_status_code(self):
        """Проверяем доступность страниц для авторизованного пользователя."""
        fields_response_urls_code = {
            reverse('posts:index'): HTTPStatus.OK,
            reverse('posts:group_list', args={self.group.slug}): HTTPStatus.OK,
            reverse('posts:post_create'): HTTPStatus.OK,
            reverse(
                'posts:profile', args={self.author.username}
            ): HTTPStatus.OK,
            reverse('posts:post_detail', args={self.post.id}): HTTPStatus.OK,
            reverse('posts:post_edit', args={self.post.id}): HTTPStatus.OK,
        }
        for adress, response_code in fields_response_urls_code.items():
            with self.subTest(adress=adress):
                status_code = self.authorized_client.get(adress).status_code
                self.assertEqual(status_code, response_code)

    def test_posts_create_for_auth(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_edit_for_author(self):
        """Страница /posts/<post_id>/edit/ доступна только авторизованному
        пользователю."""
        self.author = User.objects.get(username=self.author)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)
        response = self.authorized_client.get(
            reverse('posts:post_edit', args={self.post.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_create_redirect_for_guest(self):
        """Страница /create/ перенаправляет неавторизованного пользователя."""
        response = self.guest_client.get(reverse('posts:post_create'))
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )

    def test_posts_edit_redirect_for_guest(self):
        """Страница /posts/<post_id>/edit перенаправляет неавторизованного
        пользователя."""
        response = self.guest_client.get(
            reverse('posts:post_edit', args={self.post.id})
        )
        self.assertRedirects(
            response, f'/auth/login/?next=/posts/{self.post.pk}/edit/'
        )

    def test_unexisting_page(self):
        """Несуществующая страница выдает 404 ошибку и
        отдаёт кастомный шаблон."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse(
                'posts:group_list', args={self.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', args={self.author.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail', args={self.post.id}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit', args={self.post.id}
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
