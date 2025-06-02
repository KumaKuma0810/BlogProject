from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from tinymce.widgets import TinyMCE

from .models import *

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),

        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'avatar': '',
        }

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label='Описание', widget=TinyMCE(attrs={'class':'form-control','cols': 110, 'rows': 10}))
    tags = forms.CharField(label='Тег', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите теги через запятую'}))
    img = forms.FileField(label='Изображение', widget=forms.FileInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'img']

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        # Разбиваем по запятым и убираем пробелы
        tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        return tags_list

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше сообщение',
            'rows': 5,
            'cols': 50
        }))

    class Meta:
        model = Post
        fields = ['title', 'body', 'tags']

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            tags_str = self.cleaned_data['tags']
            tags = [t.strip() for t in tags_str.split(',') if t.strip()]

            for tag_name in tags:
                tag_obj, created = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={'slug': slugify(tag_name)})
                instance.tags.add(tag_obj)

        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Оставьте комментарий...',
                'rows': 3,
                'cols': 150,
            })
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Name'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Replace password'
        })

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
