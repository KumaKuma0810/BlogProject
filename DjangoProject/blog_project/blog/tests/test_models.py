import pytest
from django.db import models

from blog.models import Post
from django.contrib.auth.models import User

# Pytest разрешает использовать базу данных в этом тесте
@pytest.mark.django_db
def test_post_creation():
    post = Post.objects.create(
        title='TestPost',
        body='Test post',
        author = 'Kuma',
        tags = 'test post, pytest post',
    )
    assert post.title == 'TestPost'
    assert post.body == 'Test post'
    assert.author = 'Kuma'
    seert.tags = 'test post'

def test_post_str(post):
    assert str(post) == 'Test post'

# db: фикстура от pytest-django для работы с базой.
@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password123')

@pytest.fixture
def post(user):
    return Post.objects.create(title='Test Post', body='Test body', author=user, tags='tags test')

@pytest.fixture
def posts(user):
    return [
        Post.objects.create(title=f'Post {i}', body='Text post', author=user, tags='tags test')
        for i in range(10)
    ]







