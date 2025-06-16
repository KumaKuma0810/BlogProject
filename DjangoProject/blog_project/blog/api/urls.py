from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', PostListAPIView.as_view()),
    path('post/<int:pk>/', PostDetailAPIView.as_view()),
]
