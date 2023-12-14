# Проект Yatube Social Network

Yatube - это веб-приложение на Django, которое позволяет пользователям публиковать свои посты, комментировать их, подписываться на других пользователей и управлять своим профилем.

## Модели

- `Post`: Модель для представления постов пользователей. Содержит текст поста, дату публикации, автора и группу.
- `Group`: Модель для представления групп, в которых пользователи могут публиковать свои посты. Содержит название, слаг и описание группы.
- `Comment`: Модель для представления комментариев к постам. Содержит текст комментария, дату создания, автора и пост.
- `Follow`: Модель для представления подписок пользователей. Содержит пользователя и автора.

## URL-маршруты

- Главная страница (`/`): Показывает последние обновления на сайте.
- Страница группы (`group/<slug:slug>/`): Показывает посты в определенной группе.
- Профиль пользователя (`profile/<str:username>/`): Показывает посты определенного пользователя.
- Детали поста (`posts/<int:post_id>/`): Показывает детали определенного поста.
- Создание поста (`create/`): Позволяет пользователям создавать новые посты.
- Редактирование поста (`posts/<int:post_id>/edit/`): Позволяет пользователям редактировать свои посты.
- Добавление комментария (`posts/<int:post_id>/comment/`): Позволяет пользователям добавлять комментарии к постам.
- Индекс подписок (`follow/`): Показывает посты авторов, на которых подписан текущий пользователь.
- Подписка на профиль (`profile/<str:username>/follow/`): Позволяет пользователям подписываться на других пользователей.
- Отписка от профиля (`profile/<str:username>/unfollow/`): Позволяет пользователям отписываться от других пользователей.

## Представления

- `index`: Представление для отображения последних обновлений на сайте.
- `group_posts`: Представление для отображения постов в определенной группе.
- `profile`: Представление для отображения профиля пользователя.
- `post_detail`: Представление для отображения деталей поста.
- `post_create`: Представление для создания нового поста.
- `post_edit`: Представление для редактирования существующего поста.
- `add_comment`: Представление для добавления комментария к посту.
- `follow_index`: Представление для отображения постов авторов, на которых подписан текущий пользователь.
- `profile_follow`: Представление для подписки на других пользователей.
- `profile_unfollow`: Представление для отписки от других пользователей.

## Тесты

- `CacheTests`: Тесты для проверки кэширования данных на главной странице.
- `FollowViewTest`: Тесты для проверки возможности пользователей подписываться на других пользователей, отписываться от них и просматривать посты авторов, на которых они подписаны.
- `PostFormTests`: Тесты для проверки создания и редактирования постов с помощью формы.
- `PostPagesTests`: Тесты для проверки корректности контекста в представлениях.
- `PostCreateFormTests`: Тесты для проверки создания поста с изображением.
- `CommentTests`: Тесты для проверки возможности пользователей комментировать посты.

## Используемые технологии

Вот краткое описание используемых технологий:

- **Python**: Язык программирования.
- **Django**: Веб-фреймворк.
- **Django Forms**: Инструмент для создания форм.
- **Django ORM**: Инструмент для работы с базой данных.
- **SQLite**: СУБД.
- **HTML/CSS**: Языки для создания и стилизации веб-страниц.
- **Django Templates**: Инструмент для генерации HTML.

## Автор

Anatolii Bessmertnyi
