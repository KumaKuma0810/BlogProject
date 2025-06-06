import pytest
from django.url import reverse

@pytest.mark.django_db
def test_post_list_pagination(client, posts):
    url = reverse('post_list') # возвращает реальный URL.
    response = client.get(url, {'page': 1})
    assert response.status_code == 200
    #.decode() — переводим байты в строку (обычно в UTF-8).
    assert 'Post 0' in response.content.decode()
