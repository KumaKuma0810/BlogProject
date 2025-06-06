import pytest

from django.urls import reverse
from .models import Post
# client - встроенный тестовый клиент Django для имитации запросов.
# @pytest.mark.django_db
# def test_post_list_view(client):
#     Post.objects.create(title='Test1', body='Test body', author='TestUser', tags='tags test')
#     Post.objects.create(title='Test2', body='Test body', author='TestUser', tags='tags test')

#     url = reverse('post_list')
#     response = client.get(url)

#     assert response.status_code == 200
#     assert 'Test1' in response.content.decode()
#     assert 'Test2' in response.content.decode()


@pytest.mark.django_db
def test_post_detail_view(client, post):
    url = reverse('post_detail', args=[post.pk])
    response = client.get(url)

    assert response.status_code == 200
    assert post.title in response.content.decode()
    assert post.body in response.content.decode()
