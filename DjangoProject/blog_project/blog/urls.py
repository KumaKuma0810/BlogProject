from django.urls import path, include
from .views import *

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

#API
from rest_framework.routers import DefaultRouter
from .views import PostSerializer

router = DefaultRouter()
router.register(r'post', PostViewSet)

urlpatterns = [
    #API
    path('api/', include(router.urls)),


    # path('test-404', page_404),
    path('comment/edit/<int:pk>', edit_comment, name='edit_comment'),
    path('edit-profile', UpdateProfile, name='edit_profile'),
    path('about', About, name='about_page'),
    path('post-archive', ArchivePost, name='post_atchive'),
    path('search', SearchPost, name='post_search'),
    path('tag/<int:tag_id>', PostsByTag, name='posts_by_tag'),

    path('post/delete/<slug:slug>', PostDeleteView.as_view(), name='post_delete'),
    path('post/edit/<slug:slug>', UpdatePost, name='post_edit'),

    path('create/', PostCreate, name='post_create'),

    path('delete-profile/', UserDeleteView.as_view(), name='delete_profile'),
    path('author/<int:pk>', AuthorDetailView.as_view(), name='author'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('signup/', signup_view, name='signup'),

    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('', PostListView.as_view(), name='post_list'),

    path('ckeditor/', include('ckeditor_uploader.urls'))

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
