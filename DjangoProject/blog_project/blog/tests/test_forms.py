import pytest
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from blog.models import Post, Tag
from blog.form import PostCreateForm

@pytest.mark.django_db
def test_post_form_creates_post_and_tags():
    user = User.objects.create_user(username='test_user', password='Vener@001')

    image = SimpleUploadedFile(
        name='test_image.jpg',
        content=b'some_image_data',
        content_type='image/jpeg'
    )

    form_data = {
        'title': 'test post',
        'body': 'Content post form',
        'tags': 'python, django, pytest',
    }

    form = PostCreateForm(data=form_data, files={'img': image})
    assert form.is_valid(), form.errors

    post = form.save(author=user)

    assert Post.objects.count() == 1
    assert post.author == user
    assert Post.objects.first().title == 'test post'

    tag_names = ['python', 'django', 'pytest']
    assert post.tags.count() == 3
    for name in tag_names:
        assert post.tags.filter(name=name).exists()

