import pytest

from django.urls import reverse

@pytest.mark.django_db
def test_create_post_requires_authentication(client):
    url = reverse('post_create')
    response = client.get(url)
    assert response.status_code == 302 #redirect in login


@pytest.mark.django_db
def test_create_post_authenticated(client, user):
    # client — тестовый клиент Django, имитирует
    # поведение браузера (можно делать запросы к сайту).
    client.login(username='testuser', password='password123')
    url = reverse('post_create')
    response = client.get(url)

    assert response.status_code == 200

@pytest.mark.django_db
def test_create_post_via_form(client, user):
    # Логинимся
    client.login(username = 'testuser', password = 'password123')
    url = reverse('post_create')
    #Данные для нового поста
    data = {
        'title': 'New test post',
        'content': 'this is the content of the new post'
        'author': user.id,
        'tags': 'new test tags'
    }

    response = client.post(url, data)
    # проверяем что после создания происходит редирект
    assert response.status_code == 302
    # проверяем что пост появился в базе
    post = Post.objects.filter(
        'title': 'New test post',
        'content': 'this is the content of the new post'
        'author': user.id,
        'tags': 'new test tags'
    ).first()

    assert post in not None
    assert post.title == 'New test post'
    assert post.content == "this is the content of the new post"
    assert post.author == user

