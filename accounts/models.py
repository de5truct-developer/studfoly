from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Тёмная'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile',
        verbose_name='Пользователь'
    )
    avatar = models.ImageField(
        'Аватар', upload_to='avatars/', blank=True, null=True
    )
    bio = models.TextField('О себе', blank=True)
    title = models.CharField(
        'Роль/Специализация', max_length=200, blank=True,
        help_text='Например: Frontend Developer'
    )
    city = models.CharField('Город', max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    telegram = models.CharField('Telegram', max_length=100, blank=True)
    github = models.URLField('GitHub', blank=True)
    linkedin = models.URLField('LinkedIn', blank=True)
    website = models.URLField('Сайт', blank=True)
    skills_summary = models.TextField('Краткое описание навыков', blank=True)
    is_available = models.BooleanField(
        'Доступен для работы/проектов', default=False
    )
    theme_preference = models.CharField(
        'Тема оформления', max_length=10, choices=THEME_CHOICES, default='light'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль {self.user.get_full_name() or self.user.username}'

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username
