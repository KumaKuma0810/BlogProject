import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_api_post_list(client, posts):
    url = reverse('api:post-list')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(posts)

@pytest.mark.django_db
def test_api_create_required_auth(client):
    url = reverse('api:post-list')
    response = client.post(url, {'title': 'API', 'content': 'test'})
    assert response.status_code == 403 or response.status_code == 401
