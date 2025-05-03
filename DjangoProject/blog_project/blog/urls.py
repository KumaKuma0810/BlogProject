from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('tag/<int:id>', PostsByTag, name='posts_by_tag'),

    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('post/edit/<int:pk>', UpdatePost, name='post_edit'),

    path('create/', PostCreate, name='post_create'),

    path('delete-profile/', UserDeleteView.as_view(), name='delete_profile'),
    path('author/<int:pk>', AuthorDetailView.as_view(), name='author'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('signup/', signup_view, name='signup'),

    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('', PostListView.as_view(), name='post_list'),
]
