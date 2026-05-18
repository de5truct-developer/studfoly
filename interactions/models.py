from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Пользователь'
    )
    project = models.ForeignKey(
        'portfolio.Project', on_delete=models.CASCADE, related_name='comments',
        verbose_name='Проект'
    )
    text = models.TextField('Текст комментария')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='replies', verbose_name='Родительский комментарий'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.text[:50]}'


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes',
        verbose_name='Пользователь'
    )
    project = models.ForeignKey(
        'portfolio.Project', on_delete=models.CASCADE, related_name='likes',
        verbose_name='Проект'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'project')

    def __str__(self):
        return f'{self.user.username} -> {self.project.title}'


class Bookmark(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookmarks',
        verbose_name='Пользователь'
    )
    project = models.ForeignKey(
        'portfolio.Project', on_delete=models.CASCADE, related_name='bookmarks',
        verbose_name='Проект'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'
        unique_together = ('user', 'project')

    def __str__(self):
        return f'{self.user.username} -> {self.project.title}'


class ProfileView(models.Model):
    viewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='profile_views_made',
        verbose_name='Просматривающий'
    )
    viewed_profile = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='profile_views_received',
        verbose_name='Просмотренный профиль'
    )
    created_at = models.DateTimeField('Дата просмотра', auto_now_add=True)

    class Meta:
        verbose_name = 'Просмотр профиля'
        verbose_name_plural = 'Просмотры профилей'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.viewer.username} -> {self.viewed_profile.username}'
