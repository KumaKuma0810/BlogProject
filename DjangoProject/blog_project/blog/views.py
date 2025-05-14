from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django .contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, DeleteView
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.core.paginator import Paginator

from .form import *
from .models import *


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user != request.user:
        return redirect('post_detail', comment.post.slug)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()

            return redirect('post_detail', comment.post.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})




@login_required
def UpdateProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # или куда нужно
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'blog/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# def page_404(request):
#     return render(request, 'blog/404.html')

def About(request):
    return render(request, 'blog/about.html')


def ArchivePost(request):
    post_list = Post.objects.filter(published=False)
    paginator = Paginator(post_list, 4)
    page_num = request.GET.get('page')  # Получаем текущую страницу из GET-запроса
    page_obj = paginator.get_page(page_num)

    return render(request, 'blog/post_archive.html', {'posts': page_obj})


def SearchPost(request):
    query = request.GET.get('q', '')  # Получаем запрос из строки ?q=...
    res = []

    if query:
        res = Post.objects.filter(title__icontains=query)    #__icontains "регистронезависимое содержит" (нечёткий поиск)

    return render(request, 'blog/search_post.html', {'query': query, 'results': res})


@login_required
def PostCreate(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            tags_list = form.cleaned_data['tags']

            post = Post.objects.create(author=request.user, title=title, body=body)

            for tag_name in tags_list:
                tag_slug = slugify(tag_name)
                tag, created = Tag.objects.get_or_create(name=tag_name, slug=tag_slug)
                post.tags.add(tag)

            post.save()
            return redirect('/')
    else:
        form = PostCreateForm()
    return render(request, 'blog/post_create.html', {'form': form})


@login_required
def UpdatePost(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user:
        return redirect('post_detail', slug)

    if request.method == 'POST':
        form = PostCreateForm(request.POST)

        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.save()

            tags_list = form.cleaned_data['tags']
            post.tags.clear()                   # Очищаем текущие теги

            for tag_name in tags_list:
                tag_slug = slugify(tag_name)
                tag, created = Tag.objects.get_or_create(name=tag_name, slug=tag_slug)
                post.tags.add(tag)

            return redirect('post_detail', slug=slug)
    else:
        initial_tags = ', '.join(tag.name for tag in post.tags.all())
        form = PostCreateForm(initial = {
            'title': post.title,
            'body': post.body,
            'tags': initial_tags,
        })

    return render(request, 'blog/post_edit.html', {'form':form})


def PostsByTag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    posts = Post.objects.filter(tags=tag, published=True)

    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})


#UserPassesTestMixin - позволяет задать дополнительную проверку через test_func()
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'blog/user_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        profile = user.profile
        posts = Post.objects.filter(author=user, published=True)

        context['user'] = user
        context['profile'] = profile
        context['posts'] = posts

        return context


def custom_logout(request):
    logout(request)
    return redirect('post_list')


def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
                return redirect('post_list')
            else:
                messages.error(request, 'Incorrect login or password')
    else:
        form = CustomLoginForm()
    return render(request, 'blog/registration/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user=form.save()
            Profile.objects.create(user=user)
            login(request, user)

            return redirect('/')
    else:
        form=SignUpForm()

    return render(request, 'blog/registration/signup.html', {'form': form})


class PostListView(ListView):
    model = Post
    template_name='blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    # для расширения контекста
        context['form'] = CommentForm()                 # Добавляем пустую форму комментария

        #self.object — текущий пост.
        #.comments — это related_name, заданный в модели Comment в поле post = ForeignKey(...)
        #select_related('user') — чтобы одним SQL-запросом загрузить и пользователя,
        #   написавшего комментарий, без лишних запросов
        context['comments'] = self.object.comments.select_related('user')
        return context

        #за обработку отправки формы
    def post(self, request, *args, **kwargs):
        # Получаем текущий пост self.object нужен, чтобы связать комментарий с ним.
        # DetailView сам вызывает get_object() и сохраняет результат в self.object
        # перед тем, как вызвать get_context_data() и отрендерить шаблон.
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            # commit=False - Не сохраняй в базу сразу, я ещё не всё заполнил
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()

            return redirect(self.object.get_absolute_url())

        context = self.get_context_data()
        context['form'] = form

        return self.render_to_response(context)


class AuthorDetailView(DetailView):
    model = User
    template_name = 'blog/author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Все посты пользователя
        context['posts'] = Post.objects.filter(author=self.object, published=True)
        # Профиль пользователя (avatar, bio и т.д.)
        context['profile'] = self.object.profile

        return context

