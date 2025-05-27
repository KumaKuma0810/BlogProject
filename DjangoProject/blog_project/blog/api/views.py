from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.pagination import PageNumberPagination

class PostListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        posts = Post.objects.all()
        search_query = request.query_params.get('search', None)
        if search_query:
# title__icontains — заголовок содержит (без учёта регистра)
# content__icontains — содержимое содержит search_query.
            posts = posts.filter(Q(title__icontains=search_query) | Q(content_icontains=search_query))

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(posts, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data = request.data)

# Получаем данные от клиента в формате JSON (request.data) и передаём в сериализатор.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PostDetailAPIView(APIView):
# Разрешения: неавторизованные могут только читать, авторизованные — создавать.
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

# Получаем пост по pk.
# Сериализуем объект.
# Отправляем данные клиенту.
    def get(self, request, pk):
        post = self.get_object(pk)

        if not post:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response(serializer.data)

# Получаем существующий пост.
# Передаём в сериализатор текущий объект и новые данные из запроса — так
# сериализатор понимает, что это обновление.
    def put(self, request, pk):
        post = self.get_object(pk)

        if not post:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
