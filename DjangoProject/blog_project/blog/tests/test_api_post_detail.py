import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from blog.models import Post

@pytest.mark.django_db
def test_post_detail_get():
    user = User.objects.create_user(username='test_api_user', password='Vener@001')
    post = Post.objects.create(title='Test title', body='test post', author=user)

    client = APIClient()
    response = client.get(f'/api/v1/post/{post.pk}/')

    assert response.status_code == 200
    assert response.data['title'] == 'Test title'


@pytest.mark.django_db
def test_post_detail_put():
    user = User.objects.create_user(username='test_api_user', password='Vener@001')
    post = Post.objects.create(title='Old title', body='Old post', author=user)

    client = APIClient()
    client.force_authenticate(user=user)

    payload = {
        'title': 'New title',
        'body': 'Update body',
        'author': user.pk
    }

    response = client.put(f'/api/v1/post/{post.pk}/', data=payload, format='json')

    assert response.status_code == 200
    assert response.data['title'] == 'New title'
    # refresh_from_db - метод модели Django, который перечитывает данные из базы данных,
    # полностью обновляя объект в памяти.
    post.refresh_from_db()
    assert post.title == 'New title'

    # Разрешает этому тесту работать с базой данных (создавать и удалять записи).


@pytest.mark.django_db
def test_post_detail_delete():
    user = User.objects.create_user(username='test_api_user', password='Vener@001')
    post = Post.objects.create(title='Old title', body='Old post', author=user)
    # Будет отправлять HTTP-запросы в тесте
    client = APIClient()
    # Это имитация входа в систему — теперь client считается "залогиненным"
    client.force_authenticate(user=user)
    # Отправляется DELETE-запрос на URL
    response = client.delete(f'/api/v1/post/{post.pk}/')
    # Убеждаемся, что сервер ответил 204 No Content
    assert response.status_code == 204
    # Проверяем, что пост действительно удалён из базы данных.
    assert not Post.objects.filter(pk=post.pk).exists()
