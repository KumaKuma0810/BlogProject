from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
# from ckeditor_uploader.fields import RichTextUploadingField
from tinymce.models import HTMLField

class AboutModel(models.Model):
    text = HTMLField(blank=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=False)

    def save(self, *args, **kwargs):                # переопределяем метод save
        if not self.slug:                           # проверяем, есть ли уже у поста slug
            base_slug = slugify(self.name)          # с помощью функции slugify преобразуем заголовок поста в слуг
            slug = base_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('tag_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField('')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"comment on {self.user.username} '{self.post.title}'"


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = HTMLField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):    #переопределяем метод save
        if not self.slug:   #проверяем, есть ли уже у поста slug
            base_slug = slugify(self.title) #с помощью функции slugify преобразуем заголовок поста в слуг
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exists(): #проверяем, существует ли уже в базе данных пост с таким же slug
                slug = f"{base_slug}-{counter}" #создаём новый slug, добавляя к базовому slug число
                counter += 1
            self.slug = slug    #назначаем сгенерированный slug нашему объекту Post.
        # вызываем оригинальный метод save из родительского класса models.Model, чтобы сохранить
        # объект с уже сгенерированным значением slug.
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"
