from django.contrib import admin
from .models import Post, Place, Page, Author, Category, Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
    # list_display = ('title',)
    # ordering = ('title',)
    # search_fields = ('title',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)
    search_fields = ('title',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'title',)
    ordering = ('page_name',)
    search_fields = ('page_name',)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)