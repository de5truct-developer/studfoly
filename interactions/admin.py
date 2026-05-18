from django.contrib import admin
from .models import Comment, Like, Bookmark, ProfileView


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'short_text', 'parent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'project__title')
    raw_id_fields = ('user', 'project', 'parent')

    def short_text(self, obj):
        return obj.text[:60]
    short_text.short_description = 'Текст'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('user', 'project')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('user', 'project')


@admin.register(ProfileView)
class ProfileViewAdmin(admin.ModelAdmin):
    list_display = ('viewer', 'viewed_profile', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('viewer', 'viewed_profile')
