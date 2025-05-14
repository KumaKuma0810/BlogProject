from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls'))
]
# Это нужно ТОЛЬКО в режиме разработки
if settings.DEBUG:
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('tinymce/', include('tinymce.urls')),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
