import pytest
from rest_framework import APIClient
from django.contrib.auth.models import User

from blog.models import Post

@pytest.mark.django_db
def test_post_all():
    user = User.objects.create(username='test_user', password='Vener@001')
    post = Post.objects.all()

    client = APIClient()
    response = client.get(f'/api/v1/posts/')

    assert response.status_code == 200
