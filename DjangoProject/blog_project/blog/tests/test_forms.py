from blog.forms import PostCreateForm

def test_valid_form(user):
    form_data = {
        "title":"TestPost",
        "body":"Test post",
        "author": user.id,
        "tags": "test post, pytest post",
    }
    form = PostCreateForm(data = form_data)
    assert form.is_valid()

def test_invalid_post_form():
    form_data = {
        "title":"TestPost",
        "body":"Test post 2",
    }

    assert not form.is_valid()
    assert 'title' in form.errors
    assert 'body' in form.errors


