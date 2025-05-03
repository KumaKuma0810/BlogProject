from django.contrib import admin
from .models import *

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'body')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'avatar')

